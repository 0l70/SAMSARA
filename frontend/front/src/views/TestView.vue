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
        <button class="signup-btn" @click="goToSignup">
          나에게 딱 맞는 상품 추천받기 (가입)
        </button>
        <button class="retry-btn" @click="resetTest">다시 하기</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ---------------------------------------------------------
// 상태 변수
// ---------------------------------------------------------
const step = ref(-1) // -1: 시작전, 0~11: 질문중, 12: 결과
const score = ref(0)
const result = ref({})

// ---------------------------------------------------------
// 질문 데이터 (1점 vs 3점)
// ---------------------------------------------------------
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

// ---------------------------------------------------------
// 로직 함수
// ---------------------------------------------------------
const startTest = () => {
  step.value = 0
  score.value = 0
}

const selectAnswer = (points) => {
  score.value += points
  step.value++
  
  if (step.value === questions.length) {
    calculateResult()
  }
}

const calculateResult = () => {
  const s = score.value
  
  if (s <= 17) {
    result.value = {
      type: 'safe',
      icon: '🐜',
      title: '성실한 개미',
      desc: '티끌 모아 태산! 원금 보장이 최우선인 당신은 차곡차곡 자산을 쌓아가는 안정형 투자자입니다.',
      advice: '최고 금리 적금과 예금 상품을 추천해 드려요.'
    }
  } else if (s <= 23) {
    result.value = {
      type: 'neutral',
      icon: '🐹',
      title: '신중한 햄스터',
      desc: '돌다리도 두들겨 보고 건너요. 안정성을 추구하면서도 소소한 수익을 놓치지 않는 균형 잡힌 투자자입니다.',
      advice: '채권형 펀드나 저위험 중수익 상품이 딱 맞아요.'
    }
  } else if (s <= 29) {
    result.value = {
      type: 'active',
      icon: '🦊',
      title: '똑똑한 여우',
      desc: '하이 리스크, 하이 리턴! 위험을 감수하더라도 높은 수익을 노리는 스마트한 투자자입니다.',
      advice: 'ETF나 주식형 펀드, 고금리 상품을 분석해 보세요.'
    }
  } else {
    result.value = {
      type: 'aggressive',
      icon: '🦁',
      title: '용감한 사자',
      desc: '인생은 한 방! 과감한 결단력으로 시장을 주도하는 공격적인 투자자입니다.',
      advice: '공격적인 주식 투자와 비상금 파킹통장 조합을 추천해요.'
    }
  }
}

const resetTest = () => {
  step.value = -1
  score.value = 0
}

// ★ 핵심: 회원가입 페이지로 결과 들고 이동하기
const goToSignup = () => {
  // query로 mbti 정보를 넘깁니다. (예: /signup?mbti=safe)
  router.push({ name: 'signup', query: { mbti: result.value.type } })
}
</script>

<style scoped>
/* 전체 레이아웃 */
.test-container {
  max-width: 500px; margin: 50px auto; padding: 40px 30px;
  background: white; border-radius: 24px; text-align: center;
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

/* 1. 인트로 */
.intro-slide .icon { font-size: 80px; margin-bottom: 20px; }
.intro-slide h1 { font-size: 1.8rem; font-weight: 800; color: #333; margin-bottom: 10px; }
.intro-slide p { color: #666; margin-bottom: 40px; line-height: 1.6; }
.start-btn {
  width: 100%; padding: 16px; font-size: 1.2rem; font-weight: 700;
  background: #3b82f6; color: white; border: none; border-radius: 12px; cursor: pointer;
  transition: background 0.2s;
}
.start-btn:hover { background: #2563eb; }

/* 2. 질문 화면 */
.progress-bar { width: 100%; height: 8px; background: #eee; border-radius: 4px; margin-bottom: 15px; overflow: hidden; }
.fill { height: 100%; background: #3b82f6; transition: width 0.3s ease; }
.step-count { font-size: 0.9rem; color: #999; font-weight: 600; }
.question-text { font-size: 1.4rem; font-weight: 700; color: #222; margin: 30px 0 50px; line-height: 1.4; word-break: keep-all;}

.choices { display: flex; flex-direction: column; gap: 15px; }
.choice-btn {
  padding: 20px; border: 2px solid #e5e7eb; border-radius: 16px; background: white;
  font-size: 1rem; color: #4b5563; cursor: pointer; text-align: left; transition: all 0.2s;
  display: flex; align-items: center;
}
.choice-btn:hover { border-color: #3b82f6; background: #eff6ff; color: #3b82f6; }
.choice-btn .label {
  display: inline-flex; width: 28px; height: 28px; background: #e5e7eb; color: #666;
  border-radius: 50%; font-size: 0.8rem; font-weight: bold; justify-content: center; align-items: center; margin-right: 12px;
}
.choice-btn:hover .label { background: #3b82f6; color: white; }

/* 3. 결과 화면 */
.subtitle { color: #666; font-size: 1rem; margin-bottom: 10px; }
.result-icon { font-size: 80px; margin-bottom: 10px; }
.result-title { font-size: 2rem; font-weight: 900; color: #3b82f6; margin-bottom: 20px; }
.result-desc { color: #4b5563; line-height: 1.6; margin-bottom: 30px; word-break: keep-all; }

.recommend-box {
  background: #f3f4f6; padding: 20px; border-radius: 16px; margin-bottom: 30px;
}
.recommend-box h3 { margin: 0 0 10px; color: #1f2937; font-size: 1.1rem; }
.recommend-box p { margin: 0; color: #4b5563; font-size: 0.95rem; }

.signup-btn {
  width: 100%; padding: 16px; font-size: 1.1rem; font-weight: 700;
  background: #10b981; color: white; border: none; border-radius: 12px; cursor: pointer;
  margin-bottom: 10px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}
.signup-btn:hover { background: #059669; }
.retry-btn {
  width: 100%; padding: 14px; font-size: 1rem; font-weight: 600;
  background: white; color: #666; border: 1px solid #ddd; border-radius: 12px; cursor: pointer;
}
.retry-btn:hover { background: #f9fafb; }
</style>