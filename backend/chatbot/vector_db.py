import os
# import shutil  <-- ❌ 이제 삭제 모듈은 안 씁니다
from django.conf import settings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from products.models import DepositProducts, SavingProducts

# SSAFY GMS 설정
GMS_BASE_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

def build_vector_db():
    print("⏳ [FinBot] 금융 상품 데이터가 변경되었습니다. Vector DB를 재구축합니다...")
    
    persist_directory = os.path.join(settings.BASE_DIR, 'chroma_db')
    
    # 임베딩 모델
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=settings.OPENAI_API_KEY,
        base_url=GMS_BASE_URL
    )

    # 1. DB 연결 (없으면 생성됨)
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    # ---------------------------------------------------------
    # ★ [수정] 폴더 삭제 대신 "내용물(ID) 조회 후 삭제" (Windows Lock 방지)
    # ---------------------------------------------------------
    existing_data = vector_store.get() # 현재 DB에 있는 모든 데이터 조회
    if existing_data['ids']:
        print(f"🧹 기존 데이터 {len(existing_data['ids'])}개를 삭제하고 초기화합니다...")
        vector_store.delete(ids=existing_data['ids']) # 깔끔하게 내용만 비움
    else:
        print("✨ 기존 DB가 비어있습니다. 새로 구축합니다.")


    # 2. SQL DB 데이터 가져오기 (옵션 포함)
    deposits = DepositProducts.objects.all().prefetch_related('options')
    savings = SavingProducts.objects.all().prefetch_related('options')
    
    docs = []

    # 3. 예금 데이터 처리
    for p in deposits:
        options_str = ""
        for opt in p.options.all():
            options_str += f"{opt.save_trm}개월: {opt.intr_rate}% / "
        
        content = f"""
        [상품명] {p.fin_prdt_nm}
        [은행] {p.kor_co_nm}
        [유형] 정기예금
        [가입방법] {p.join_way}
        [우대조건] {p.spcl_cnd}
        [금리정보] {options_str}
        """
        metadata = {"type": "deposit", "bank": p.kor_co_nm, "pk": p.pk}
        docs.append(Document(page_content=content.strip(), metadata=metadata))

    # 4. 적금 데이터 처리
    for p in savings:
        options_str = ""
        for opt in p.options.all():
            options_str += f"{opt.save_trm}개월: {opt.intr_rate}% / "

        content = f"""
        [상품명] {p.fin_prdt_nm}
        [은행] {p.kor_co_nm}
        [유형] 적금
        [가입방법] {p.join_way}
        [우대조건] {p.spcl_cnd}
        [금리정보] {options_str}
        """
        metadata = {"type": "saving", "bank": p.kor_co_nm, "pk": p.pk}
        docs.append(Document(page_content=content.strip(), metadata=metadata))

    if not docs:
        print("⚠️ 저장된 금융 상품 데이터가 없습니다.")
        return

    print(f"📊 총 {len(docs)}개의 데이터를 저장합니다.")

    # ---------------------------------------------------------
    # 5. 데이터 저장 (배치 사이즈 30 유지 - 413 에러 방지)
    # ---------------------------------------------------------
    batch_size = 30  
    total_docs = len(docs)

    for i in range(0, total_docs, batch_size):
        batch = docs[i : i + batch_size]
        vector_store.add_documents(batch)
        print(f"   ↳ 진행 중... ({min(i + batch_size, total_docs)}/{total_docs})")
    
    print(f"✅ [FinBot] Vector DB 업데이트 완료! (총 {len(docs)}개 상품)")