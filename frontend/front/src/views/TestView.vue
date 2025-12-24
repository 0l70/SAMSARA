<template>
  <div class="test-container">
    
    <div v-if="step === -1" class="intro-slide">
      <div class="icon">💰</div>
      <h1>나의 금융 성향 테스트</h1>
      <p>나는 어떤 투자자일까?<br>1분 만에 알아보는 금융 MBTI</p>
      <button class="start-btn" @click="startTest">테스트 시작하기</button>
    </div>

    <div v-else-if="step < questions.length" class="question-slide">
      <div class="progress-bar">
        <div class="fill" :style="{ width: ((step + 1) / questions.length) * 100 + '%' }"></div>
      </div>
      <span class="step-count">Q{{ step + 1 }} / {{ questions.length }}</span>

      <h2 class="question-text">{{ questions[step].q }}</h2>

      <div class="choices">
        <button class="choice-btn" @click="selectAnswer(1)">
          <span class="label">A</span>
          {{ questions[step].a }}
        </button>
        <button class="choice-btn" @click="selectAnswer(3)">
          <span class="label">B</span>
          {{ questions[step].b }}
        </button>
      </div>
    </div>

    <div v-else class="result-slide">
      <p class="subtitle">당신의 금융 성향은...</p>
      <div class="result-icon">{{ result.icon }}</div>
      <h1 class="result-title">{{ result.title }}</h1>
      <p class="result-desc">{{ result.desc }}</p>

      <div class="recommend-box">
        <h3>💡 FinBot의 제안</h3>
        <p>{{ result.advice }}</p>
      </div>

      <div class="action-buttons">
        <button class="primary-btn" @click="handleResultAction">
          {{ store.token ? '결과 저장하고 AI 비서와 상담하기 🤖' : '나에게 딱 맞는 상품 추천받기 (가입) 🎁' }}
        </button>
        
        <button class="retry-btn" @click="resetTest">다시 하기</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // 스토어 임포트

const router = useRouter()
const store = useAuthStore() // 로그인 상태 확인용

const step = ref(-1)
const score = ref(0)
const result = ref({})

const questions = [
  { q: "월급이 들어왔다! 가장 먼저 하는 일은?", a: "자동이체로 적금/저축부터 한다.", b: "카드값 갚고 사고 싶던 물건을 산다." },
  { q: "친구들과의 모임, 결제할 때 나는?", a: "10원 단위까지 정확하게 1/N 한다.", b: "기분이다! 내가 한턱 쏜다." },
  { q: "편의점에서 2+1 상품을 발견했다.", a: "당장 필요 없으면 안 산다.", b: "어차피 쓸 거니까 산다." },
  { q: "나에게 '돈'이란?", a: "안 쓰면 버는 것. 모으는 게 최고다.", b: "쓰려고 버는 것. 불리는 게 최고다." },
  { q: "1억 원이 생겼다. 어떻게 할까?", a: "잃으면 안 돼. 은행 예금에 넣는다.", b: "인생 역전! 주식이나 코인에 투자한다." },
  { q: "금융 상품 가입 시 가장 중요한 건?", a: "원금 보장이 되나요? (안정성)", b: "수익률이 몇 %인가요? (수익성)" },
  { q: "내 주식이 -20% 폭락했다.", a: "잠이 안 온다. 당장 손절한다.", b: "바겐세일이네? 물타기(추가매수) 한다." },
  { q: "친구가 '이 코인 대박'이라며 추천했다.", a: "위험해. 듣지 않고 무시한다.", b: "솔깃해서 정보를 찾아본다." },
  { q: "수익률 3% 확정 vs -10% ~ +30% 변동", a: "마음 편한 3% 확정 예금", b: "대박 가능성 있는 변동 상품" },
  { q: "여행 계획을 짤 때 나는?", a: "엑셀로 예산과 일정을 꼼꼼히 짠다.", b: "일단 비행기 표부터 끊고 본다." },
  { q: "현재 나의 노후 준비 상태는?", a: "연금 저축 등 차근차근 준비 중이다.", b: "당장 살기도 바쁘다. 나중에 생각한다." },
  { q: "대출에 대한 나의 생각은?", a: "빚은 무조건 나쁜 것. 빨리 갚자.", b: "감당 가능하면 대출도 자산이다." },
]

const startTest = () => { step.value = 0; score.value = 0 }

const selectAnswer = (points) => {
  score.value += points
  step.value++
  if (step.value === questions.length) calculateResult()
}

const calculateResult = () => {
  const s = score.value
  if (s <= 17) {
    result.value = { type: 'safe', icon: '🐜', title: '성실한 개미', desc: '티끌 모아 태산! 원금 보장이 최우선인 당신은 차곡차곡 자산을 쌓아가는 안정형 투자자입니다.', advice: '최고 금리 적금과 예금 상품을 추천해 드려요.' }
  } else if (s <= 23) {
    result.value = { type: 'neutral', icon: '🐹', title: '신중한 햄스터', desc: '돌다리도 두들겨 보고 건너요. 안정성을 추구하면서도 소소한 수익을 놓치지 않는 균형 잡힌 투자자입니다.', advice: '채권형 펀드나 저위험 중수익 상품이 딱 맞아요.' }
  } else if (s <= 29) {
    result.value = { type: 'active', icon: '🦊', title: '똑똑한 여우', desc: '하이 리스크, 하이 리턴! 위험을 감수하더라도 높은 수익을 노리는 스마트한 투자자입니다.', advice: 'ETF나 주식형 펀드, 고금리 상품을 분석해 보세요.' }
  } else {
    result.value = { type: 'aggressive', icon: '🦁', title: '용감한 사자', desc: '인생은 한 방! 과감한 결단력으로 시장을 주도하는 공격적인 투자자입니다.', advice: '공격적인 주식 투자와 비상금 파킹통장 조합을 추천해요.' }
  }
}

const resetTest = () => { step.value = -1; score.value = 0 }

// ★ 핵심 기능: 로그인 여부에 따라 동작 분기
const handleResultAction = async () => {
  // 1. 이미 로그인 된 사용자라면? -> DB 업데이트 후 챗봇으로 이동
  if (store.token) {
    try {
      await axios.patch(`${store.API_URL}/api/v1/accounts/user/`, 
        { mbti: result.value.type }, 
        { headers: { Authorization: `Token ${store.token}` } }
      )
      alert('금융 성향이 저장되었습니다! AI 비서에게 안내해 드릴게요.')
      router.replace({ name: 'chatbot' }) // 챗봇으로 바로 납치
    } catch (err) {
      console.error(err)
      alert('결과 저장 중 오류가 발생했습니다.')
    }
  } 
  // 2. 비로그인 사용자라면? -> 회원가입 페이지로 이동
  else {
    router.push({ name: 'signup', query: { mbti: result.value.type } })
  }
}
</script>

<style scoped>
/* =====================
  1. 전체 컨테이너 및 배경
===================== */
.test-container { 
  max-width: 500px; 
  margin: 50px auto; 
  padding: 40px 30px; 
  /* 라이트: white, 다크: var(--bg-card) */
  background: var(--bg-card); 
  border-radius: 24px; 
  text-align: center; 
  /* 다크모드에서 그림자는 더 깊고 진하게 */
  box-shadow: 0 10px 25px var(--shadow-color); 
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

/* =====================
  2. 인트로 및 텍스트 스타일
===================== */
.intro-slide .icon { font-size: 80px; margin-bottom: 20px; }
.intro-slide h1 { 
  font-size: 1.8rem; 
  font-weight: 800; 
  color: var(--text-primary); /* #333 -> 변수 */
  margin-bottom: 10px; 
}
.intro-slide p { 
  color: var(--text-secondary); /* #666 -> 변수 */
  margin-bottom: 40px; 
  line-height: 1.6; 
}

/* =====================
  3. 진행바 및 질문 영역
===================== */
.progress-bar { 
  width: 100%; 
  height: 8px; 
  background: var(--border-color); /* #eee -> 변수 */
  border-radius: 4px; 
  margin-bottom: 15px; 
  overflow: hidden; 
}
.fill { height: 100%; background: #3b82f6; transition: width 0.3s ease; }
.step-count { font-size: 0.9rem; color: var(--text-muted); font-weight: 600; }

.question-text { 
  font-size: 1.4rem; 
  font-weight: 700; 
  color: var(--text-primary); /* #222 -> 변수 */
  margin: 30px 0 50px; 
  line-height: 1.4; 
  word-break: keep-all;
}

/* =====================
  4. 선택지 버튼 (디자인 유지 + 다크 대응)
===================== */
.choices { display: flex; flex-direction: column; gap: 15px; }
.choice-btn { 
  padding: 20px; 
  border: 2px solid var(--border-color); /* #e5e7eb -> 변수 */
  border-radius: 16px; 
  background: var(--bg-card); 
  font-size: 1rem; 
  color: var(--text-secondary); /* #4b5563 -> 변수 */
  cursor: pointer; 
  text-align: left; 
  transition: all 0.2s; 
  display: flex; 
  align-items: center; 
}

.choice-btn:hover { 
  border-color: #3b82f6; 
  background: var(--bg-badge); /* 다크모드 호버 배경 */
  color: #3b82f6; 
}

.choice-btn .label { 
  display: inline-flex; 
  width: 28px; 
  height: 28px; 
  background: var(--border-color); 
  color: var(--text-muted); 
  border-radius: 50%; 
  font-size: 0.8rem; 
  font-weight: bold; 
  justify-content: center; 
  align-items: center; 
  margin-right: 12px; 
}
.choice-btn:hover .label { background: #3b82f6; color: white; }

/* =====================
  5. 결과 페이지 요소
===================== */
.subtitle { color: var(--text-muted); font-size: 1rem; margin-bottom: 10px; }
.result-icon { font-size: 80px; margin-bottom: 10px; }
.result-title { font-size: 2rem; font-weight: 900; color: #3b82f6; margin-bottom: 20px; }
.result-desc { 
  color: var(--text-secondary); 
  line-height: 1.6; 
  margin-bottom: 30px; 
  word-break: keep-all; 
}

.recommend-box { 
  background: var(--bg-body); /* 배경보다 약간 더 짙거나 연한 톤 */
  padding: 20px; 
  border-radius: 16px; 
  margin-bottom: 30px; 
  border: 1px solid var(--border-color);
}
.recommend-box h3 { margin: 0 0 10px; color: var(--text-primary); font-size: 1.1rem; }
.recommend-box p { margin: 0; color: var(--text-secondary); font-size: 0.95rem; }

/* =====================
  6. 하단 액션 버튼
===================== */
.start-btn { width: 100%; padding: 16px; font-size: 1.2rem; font-weight: 700; background: #3b82f6; color: white; border: none; border-radius: 12px; cursor: pointer; transition: background 0.2s; }
.start-btn:hover { background: #2563eb; }

.primary-btn { 
  width: 100%; 
  padding: 16px; 
  font-size: 1.1rem; 
  font-weight: 700; 
  background: #10b981; 
  color: white; 
  border: none; 
  border-radius: 12px; 
  cursor: pointer; 
  margin-bottom: 10px; 
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); 
}
.primary-btn:hover { background: #059669; }

.retry-btn { 
  width: 100%; 
  padding: 14px; 
  font-size: 1rem; 
  font-weight: 600; 
  background: var(--bg-card); 
  color: var(--text-muted); 
  border: 1px solid var(--border-color); 
  border-radius: 12px; 
  cursor: pointer; 
}
.retry-btn:hover { 
  background: var(--bg-body); 
  color: var(--text-secondary);
}
</style>