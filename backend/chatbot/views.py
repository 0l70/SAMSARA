import os
import traceback
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import ChatMessage

# LangChain 관련 임포트
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # 👈 MessagesPlaceholder 추가!
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.messages import HumanMessage, AIMessage

# SSAFY GMS 설정
GMS_BASE_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

# 1. [GET] 채팅 내역 불러오기 (프론트엔드용)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_history(request):
    messages = ChatMessage.objects.filter(user=request.user).order_by('created_at')
    data = [
        {
            'role': msg.role,
            'content': msg.content,
            'created_at': msg.created_at
        }
        for msg in messages
    ]
    return Response(data)

# 2. [POST] 통합 채팅 API (DB저장 + RAG + 히스토리)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    user_message = request.data.get('message')
    user_info = request.data.get('user_info', {})
    
    if not user_message:
        return Response({"error": "메시지를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ---------------------------------------------------------
        # 1. 사용자 질문을 먼저 DB에 저장 (기억하기)
        # ---------------------------------------------------------
        ChatMessage.objects.create(
            user=request.user, 
            role='user', 
            content=user_message
        )

        # ---------------------------------------------------------
        # 2. DB에서 과거 대화 내역 가져오기 (Context Memory)
        # ---------------------------------------------------------
        # 최근 10개 대화만 가져옴 (토큰 절약)
        recent_messages = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:10]
        # 최신순으로 가져왔으니 다시 시간순(과거->현재)으로 뒤집기
        recent_messages = reversed(recent_messages) 
        
        history_buffer = []
        for msg in recent_messages:
            if msg.role == 'user':
                history_buffer.append(HumanMessage(content=msg.content))
            else:
                history_buffer.append(AIMessage(content=msg.content))

        # ---------------------------------------------------------
        # 3. RAG (Vector DB & LLM) 설정
        # ---------------------------------------------------------
        vectordb_path = os.path.join(settings.BASE_DIR, 'chroma_db')
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=GMS_BASE_URL
        )
        vector_store = Chroma(
            persist_directory=vectordb_path,
            embedding_function=embeddings
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        llm = ChatOpenAI(
            model="gpt-5-mini", # 혹은 gpt-4o
            openai_api_key=settings.OPENAI_API_KEY,
            base_url=GMS_BASE_URL,
            temperature=0.7,
        )

        # ---------------------------------------------------------
        # 4. 프롬프트 작성 (히스토리 슬롯 추가)
        # ---------------------------------------------------------
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
            "- 사용자의 감정에 공감하고, 페르소나({mbti})에 맞는 톤으로 자연스럽고 친근하되 무례하지 않게 대화를 이어나가.\n"
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

        # ★ 프롬프트 템플릿에 History 공간(Placeholder) 만들기
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"), # 👈 여기가 과거 대화가 들어갈 자리
            ("human", "{question}"),
        ])

        # ---------------------------------------------------------
        # 5. 체인 구성 및 실행
        # ---------------------------------------------------------
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        prompt_val = prompt.partial(
            age=str(user_info.get("age", "알 수 없음")),
            gender=user_info.get("gender", "알 수 없음"),
            job=user_info.get("job", "알 수 없음"),
            mbti=user_info.get("mbti", "알 수 없음")
        )

        # 체인에 history 변수도 같이 전달하도록 구성
        rag_chain = RunnableParallel(
            {
                "context": retriever, 
                "question": RunnablePassthrough(),
                "history": lambda x: history_buffer # 👈 람다 함수로 히스토리 주입
            }
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

        # 실행 (invoke에는 질문만 넘기면 됨, history는 위에서 lambda로 주입됨)
        # 하지만 RunnableParallel 구조상 input을 dict로 넘기는 게 더 안전할 수 있음.
        # 여기서는 user_message(string)가 retriever로 바로 들어가므로 그대로 둡니다.
        result = rag_chain.invoke(user_message)
        
        ai_reply = result["answer"]

        # ---------------------------------------------------------
        # 6. AI 답변을 DB에 저장
        # ---------------------------------------------------------
        ChatMessage.objects.create(
            user=request.user, 
            role='ai', 
            content=ai_reply
        )

        return Response({
            "response": ai_reply,
            # "context": ... (디버깅용, 필요 없으면 주석 처리)
        })

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)