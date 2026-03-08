🏦 SAMSARA (삼사라) - 내 자산의 모든 것

    금융에도 성향이 있다! MBTI 기반 맞춤형 자산 관리 & AI 추천 서비스

1. 👨‍💻 팀원 정보 및 역할 분담 (Team Info)

SSAFY 12기 서울 6반 1팀
[이경민, 팀장]	

Full Stack

INFRA
	
Frontend

UI/UX

• 프로젝트 일정 및 아키텍처 설계


• Frontend: Vue 3 전반적인 구조 설계 및 컴포넌트 구현

• Map: Kakao Map API 연동 및 길찾기/필터링 로직 구현

• Design: 전체 UI/UX 디자인 및 반응형 웹 구현


[김민준]	

Backend

AI
	

• AI: LangChain + RAG 기반 챗봇 파이프라인 구축

• Prompt Eng: 페르소나 부여 및 환각 방지 시스템 프롬프트 설계

• Feature: MBTI 알고리즘 로직 구현 및 환율 계산기

• Infra: 배포 환경 구축 및 네트워크 설정

• Backend: Django DB 모델링, 금융 상품 데이터 수집(ETL)



2. 🌟 서비스 주요 기능 (Key Features)



🧩 1) 금융 성향 테스트 (Financial MBTI)

    사용자의 투자 성향을 분석하여 4가지 동물 페르소나로 분류합니다.

        🐜 성실한 개미 (Safe): 안정 지향형

        🐹 신중한 햄스터 (Neutral): 밸런스형

        🦊 똑똑한 여우 (Active): 성장 추구형

        🦁 용감한 사자 (Aggressive): 공격 투자형

    테스트 결과는 즉시 AI의 추천 알고리즘에 반영되어 맞춤형 상품을 제안합니다.

🤖 2) AI 금융 비서 'FinBot'

    단순한 챗봇이 아닙니다. 사용자의 나이, 자산, 직업, MBTI, 마이데이터 동의 여부를 기억합니다.

    복잡한 금융 용어를 쉽게 설명해주며, 사용자의 상황에 딱 맞는 예적금 상품을 대화하듯 추천해줍니다.

🗺️ 3) 스마트 뱅크 맵 (Bank Map)

    내 위치 기반으로 가장 가까운 은행 지점을 찾아줍니다.

    특정 은행(국민, 신한 등)만 골라보는 필터링 기능과 현재 위치에서의 도보/차량 길찾기를 제공합니다.

💰 4) 예적금 금리 비교 & 환율 계산

    시중 은행의 모든 예금/적금 상품을 금리순으로 비교합니다.

    실시간 환율 정보를 기반으로 여행 경비나 환테크 계산을 돕습니다.

1. 🧠 AI 추천 시스템 상세 (AI Logic)

SAMSARA의 챗봇은 RAG (Retrieval-Augmented Generation, 검색 증강 생성) 기술을 활용하여 금융 정보의 정확성을 높였습니다.

⚙️ 동작 프로세스

    데이터 임베딩 (Embedding): 금융감독원 API로 수집한 수천 개의 금융 상품 데이터를 텍스트 임베딩 모델(text-embedding-3-small)을 사용해 벡터화하여 ChromaDB에 저장합니다.

    질문 분석 & 검색 (Retriever): 사용자가 "안전한 적금 추천해줘"라고 물으면, 질문과 의미적으로 가장 유사한 상품 정보를 Vector DB에서 검색합니다.

    프롬프트 주입 (Prompt Injection):

        검색된 금융 상품 정보(Context)

        사용자 프로필 (나이, 자산, MBTI, 마이데이터 동의 여부)

        시스템 프롬프트 (페르소나 설정 및 답변 가이드라인)

        위 3가지를 LLM(GPT-4o-mini)에게 전달합니다.

    답변 생성 (Generation): AI는 사용자의 상황(예: "20대 사회초년생 개미 유형")을 고려하여 검색된 상품 중 최적의 상품을 선정하고 이유와 함께 답변합니다.

    💡 기술적 차별점:

        Hallucination 방지: "마이데이터 미동의" 유저에게는 정밀 추천을 제한하고 일반 인기 상품을 안내하도록 Conditional Prompting을 적용하여 거짓 정보를 방지했습니다.


    5. 🛠️ 기술 스택 및 ERD (Tech Stack)
   
🎨 Frontend

    Language: JavaScript (ES6+)

    Framework: Vue 3 (Composition API)

    State Management: Pinia

    Styling: CSS3, SCSS

    Http Client: Axios

💾 Backend

    Language: Python 3.9+

    Framework: Django, Django REST Framework (DRF)

    Authentication: Dj-Rest-Auth (JWT)

    Database: SQLite (Development)

🤖 AI & Data

    LLM Framework: LangChain

    Model: OpenAI GPT-4o-mini / text-embedding-3-small

    Vector Store: ChromaDB

📊 ERD (Entity Relationship Diagram)

(여기에 ERD 이미지를 캡처해서 넣거나, 주요 모델 관계를 글로 설명하세요)

    User: 사용자 기본 정보 + 금융 MBTI + 자산 정보 확장

    Product: 예금/적금 상품 정보 (금융감독원 데이터)

    Comment: 상품 리뷰 및 별점

    ChatHistory: AI와의 대화 내역 저장

 🤝 협업 방식 및 툴 (Collaboration)
  
🛠 Tools

    Notion: 회의록 작성, 아이디어 브레인스토밍, 일정 관리 (Kanban)

    GitLab / GitHub: 소스 코드 버전 관리

    Discord: 실시간 음성 채팅 및 화면 공유, 트러블 슈팅

    Figma: 와이어프레임 및 UI 프로토타이핑

🤙 Ground Rules

    Git Flow: master - develop - feature/기능명 브랜치 전략 사용

    Commit Message: [FEAT] 기능 구현, [FIX] 버그 수정 등 컨벤션 통일

    Code Review: Merge Request 시 팀원 1명 이상의 승인 필수

    Trouble Shooting: 에러 발생 시 에러 로그와 시도한 방법을 노션에 기록하여 공유