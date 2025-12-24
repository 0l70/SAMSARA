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
            model="gpt-5-mini",
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=GMS_BASE_URL,
            temperature=0.7,
        )

        # 3. 프롬프트 작성
        system_prompt = (
            "너는 금융 상품 추천 전문가 'FinBot'이야. "
            "사용자의 상황은 다음과 같아: "
            "[나이: {age}, 성별: {gender}, 직업: {job}, 투자성향: {mbti}]. "
            "\n\n"
            "너는 사용자의 질문을 분석해서 다음 **두 가지 경우 중 하나로 판단하고 행동**해야 해.\n"
            "\n"
            "### CASE 1: 일상적인 대화 (인사, 잡담, 날씨, 크리스마스, 위로 등 금융과 무관한 내용)\n"
            "- 🚫 **절대 금융 상품을 추천하거나 언급하지 마.**\n"
            "- 🚫 '마이데이터 동의' 관련 안내 문구도 출력하지 마.\n"
            "- 사용자의 감정에 공감하고, 페르소나({mbti})에 맞는 톤으로 자연스럽고 친근하게 대화를 이어나가.\n"
            "- 아래 제공된 [금융 상품 정보]는 무시해.\n"
            "\n"
            "### CASE 2: 금융/경제 관련 질문 (상품 추천, 재테크, 금리, 투자 조언 등)\n"
            "- ⚠️ **가장 먼저 개인정보 동의 여부를 확인해.**\n"
            "   - 만약 사용자 정보가 '정보제공 미동의'라면, 답변 시작 부분에 다음 문구를 넣어: "
            "     '📢 고객님은 마이데이터 제공에 동의하지 않으셔서 정밀한 맞춤 추천은 어렵습니다. 대신, 일반적인 인기 상품 정보를 바탕으로 안내해 드릴게요.'\n"
            "   - 동의했다면, 사용자 상황에 맞춰 친절하게 답변해.\n"
            "- 그 다음, 질문에 답변하고 아래 [금융 상품 정보]를 참고해서 가장 적합한 상품을 구체적으로 추천해줘.\n"
            "\n"
            "[금융 상품 정보] (금융 질문일 때만 참고):\n"
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