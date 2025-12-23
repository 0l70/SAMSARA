import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# LangChain 관련 임포트 (LCEL 방식)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings # 👈 여기가 핵심! 다시 OpenAI로 변경
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# SSAFY GMS 설정 (DB 만들 때 썼던 그 주소!)
GMS_BASE_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

@api_view(['POST'])
def chat(request):
    user_message = request.data.get('message')
    user_info = request.data.get('user_info', {})
    
    if not user_message:
        return Response({"error": "메시지를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. 벡터 DB 로드
        vectordb_path = os.path.join(settings.BASE_DIR, 'chroma_db')
        
        # ★★★ [수정 완료] DB와 똑같은 OpenAI 임베딩으로 교체 ★★★
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=GMS_BASE_URL
        )
        
        vector_store = Chroma(
            persist_directory=vectordb_path,
            embedding_function=embeddings
        )
        
        # 검색기(Retriever) 설정
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        # 2. LLM 설정 (GPT-4o-mini)
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=GMS_BASE_URL,
            temperature=0.7,
        )

        # 3. 프롬프트 작성
        system_prompt = (
            "너는 금융 상품 추천 전문가 'FinBot'이야. "
            "사용자의 상황은 다음과 같아: "
            "[나이: {age}, 성별: {gender}, 직업: {job}, 투자성향: {mbti}]. "
            "이 사용자의 성향에 맞춰서 친절하고 전문적으로 답변해줘. "
            "질문에 대한 답변을 먼저 하고, 그 뒤에 아래 제공된 [금융 상품 정보]를 참고하여 "
            "가장 적합한 상품 하나를 구체적으로 추천해줘. "
            "\n\n"
            "[금융 상품 정보]:\n"
            "{context}"
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{question}"),
        ])

        # 4. 체인 구성 (LCEL)
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # prompt에 user_info 미리 주입
        prompt_val = prompt.partial(
            age=str(user_info.get("age", "알 수 없음")),
            gender=user_info.get("gender", "알 수 없음"),
            job=user_info.get("job", "알 수 없음"),
            mbti=user_info.get("mbti", "알 수 없음")
        )

        rag_chain = RunnableParallel(
            {"context": retriever, "question": RunnablePassthrough()}
        ).assign(
            answer=(
                RunnablePassthrough.assign(
                    context=lambda x: format_docs(x["context"])
                )
                | prompt_val 
                | llm 
                | StrOutputParser()
            )
        )

        # 5. 실행
        result = rag_chain.invoke(user_message)

        return Response({
            "response": result["answer"],
            "context": [doc.page_content for doc in result["context"]]
        })

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)