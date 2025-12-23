import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import DepositProducts, SavingProducts
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

class Command(BaseCommand):
    help = '금융 상품 데이터를 벡터 DB(Chroma)에 저장합니다.'

    def handle(self, *args, **options):
        # 1. API 키 확인
        if not settings.OPENAI_API_KEY:
            self.stdout.write(self.style.ERROR('settings.py에 OPENAI_API_KEY가 없습니다!'))
            return

        # 2. 데이터 가져오기
        deposits = DepositProducts.objects.all()
        savings = SavingProducts.objects.all()
        
        docs = []

        # (기존 데이터 전처리 로직은 동일하게 유지...)
        # ---------------------------------------------------------
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
        # ---------------------------------------------------------

        self.stdout.write(f"총 {len(docs)}개의 데이터를 처리합니다.")

        # 3. 임베딩 모델 설정 (SSAFY 프록시 설정 포함)
        embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY,
            base_url="https://gms.ssafy.io/gmsapi/api.openai.com/v1" # ⚠️ 본인에게 맞는 URL 확인 필수!
        )

        # 4. 벡터 DB 초기화
        vectordb_path = os.path.join(settings.BASE_DIR, 'chroma_db')
        vector_store = Chroma(
            persist_directory=vectordb_path,
            embedding_function=embedding_model
        )

        # ★★★ [핵심 수정] 100개씩 쪼개서 저장 (Batch Processing) ★★★
        batch_size = 100 
        total_docs = len(docs)

        for i in range(0, total_docs, batch_size):
            batch = docs[i : i + batch_size]
            vector_store.add_documents(batch)
            self.stdout.write(f"진행 중... ({min(i + batch_size, total_docs)}/{total_docs})")

        self.stdout.write(self.style.SUCCESS(f'성공! 모든 데이터가 {vectordb_path}에 저장되었습니다.'))