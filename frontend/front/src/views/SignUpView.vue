<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1>회원가입</h1>
      
      <div v-if="mbtiResult" class="mbti-badge">
        <span>당신의 성향: <strong>{{ mbtiLabel }}</strong></span>
      </div>
      <p v-else class="subtitle">금융 서비스 이용을 위해 정보를 입력해주세요.</p>

      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label>아이디</label>
          <input type="text" v-model="form.username" required placeholder="아이디">
        </div>

        <div class="form-group">
          <label>비밀번호</label>
          <input type="password" v-model="form.password" required placeholder="비밀번호">
        </div>

        <div class="form-group">
          <label>비밀번호 확인</label>
          <input type="password" v-model="passwordConfirm" required placeholder="비밀번호 재입력">
        </div>

        <div class="form-group">
          <label>닉네임</label>
          <input type="text" v-model="form.nickname" placeholder="별명">
        </div>

        <hr class="divider">

        <h3 class="section-title">👤 맞춤 페르소나 설정 (필수)</h3>
        
        <div class="row">
          <div class="form-group half">
            <label>나이</label>
            <input type="number" v-model.number="form.age" placeholder="예: 25">
          </div>
          <div class="form-group half">
            <label>성별</label>
            <select v-model="form.gender">
              <option value="" disabled>선택</option>
              <option value="남성">남성</option>
              <option value="여성">여성</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>직업</label>
          <select v-model="form.job">
            <option value="" disabled>현재 상황을 선택해주세요</option>
            <option value="학생">학생 (대학생/대학원생)</option>
            <option value="직장인">직장인</option>
            <option value="자영업">자영업/프리랜서</option>
            <option value="전업주부">전업주부</option>
            <option value="전문직">전문직</option>
            <option value="무직">무직/취업준비생</option>
          </select>
        </div>

        <div class="form-group">
          <label>주요 자금 출처</label>
          <select v-model="form.income_source">
            <option value="" disabled>주로 어떤 돈을 관리하시나요?</option>
            <option value="월급">매달 들어오는 월급</option>
            <option value="용돈">부모님께 받는 용돈</option>
            <option value="사업수익">사업/영업 수익</option>
            <option value="금융소득">이자/배당 등 금융소득</option>
            <option value="기타">기타</option>
          </select>
        </div>

        <div class="agreement-box">
          <input type="checkbox" id="mydata" v-model="form.is_mydata_agreed">
          <label for="mydata">
            <strong>[선택] 마이데이터 서비스 동의</strong>
            <span class="desc">챗봇이 내 성향을 더 정확히 분석합니다.</span>
          </label>
        </div>

        <button type="submit" class="signup-btn">가입하기</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router' // useRoute 추가
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute() // URL 쿼리 읽기용
const store = useAuthStore()

const form = ref({
  username: '',
  password: '',
  nickname: '',
  age: null,
  gender: '',        // New
  job: '',           // New
  income_source: '', // New
  mbti: '',          // New (TestView에서 넘어옴)
  is_mydata_agreed: false
})
const passwordConfirm = ref('')

// MBTI 레이블 매핑 (화면 표시용)
const mbtiMap = {
  safe: '성실한 개미 🐜 (안정형)',
  neutral: '신중한 햄스터 🐹 (중립형)',
  active: '똑똑한 여우 🦊 (성장형)',
  aggressive: '용감한 사자 🦁 (공격형)'
}

const mbtiResult = computed(() => route.query.mbti)
const mbtiLabel = computed(() => mbtiMap[mbtiResult.value] || '알 수 없음')

onMounted(() => {
  // 테스트 페이지에서 넘어온 mbti 값이 있으면 폼에 자동 입력
  if (route.query.mbti) {
    form.value.mbti = route.query.mbti
  }
})

const handleSignup = async () => {
  if (form.value.password !== passwordConfirm.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 필수값 체크 (age, gender, job, income_source)
  if (!form.value.age || !form.value.gender || !form.value.job || !form.value.income_source) {
    alert('모든 필수 정보를 입력해주세요.')
    return
  }

  try {
    const payload = {
      username: form.value.username,
      password1: form.value.password,
      password2: passwordConfirm.value,
      nickname: form.value.nickname,
      age: form.value.age,
      gender: form.value.gender,             // 추가
      job: form.value.job,                   // 추가
      income_source: form.value.income_source, // 추가
      mbti: form.value.mbti || 'neutral',    // 없으면 기본값(중립)
      is_mydata_agreed: form.value.is_mydata_agreed
    }

    const url = store.API_URL 
      ? `${store.API_URL}/api/v1/accounts/signup/`
      : 'http://127.0.0.1:8000/api/v1/accounts/signup/'
      
    await axios.post(url, payload)
    
    alert('환영합니다! 이제 FinBot과 대화해보세요.')
    router.push({ name: 'login' })
    
  } catch (error) {
    console.error(error)
    alert('회원가입 실패: 입력 정보를 확인해주세요.')
  }
}
</script>

<style scoped>
/* 기존 스타일 유지 + 추가 스타일 */
.signup-container { display: flex; justify-content: center; align-items: center; min-height: 90vh; background-color: #f5f7fa; padding: 20px; }
.signup-card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 450px; }

/* MBTI 뱃지 */
.mbti-badge {
  background-color: #eff6ff; color: #3b82f6; text-align: center;
  padding: 10px; border-radius: 8px; margin-bottom: 20px; font-size: 0.95rem; border: 1px solid #dbeafe;
}

h1 { margin-bottom: 10px; color: #1f2937; text-align: center; font-size: 2rem; font-weight: 800; }
.subtitle { text-align: center; color: #6b7280; margin-bottom: 30px; font-size: 0.95rem; }

.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 0.95rem; }
.form-group input, .form-group select { 
  width: 100%; padding: 12px; border: 1px solid #d1d5db; border-radius: 8px; 
  font-size: 1rem; box-sizing: border-box; transition: border 0.2s; background-color: white;
}
.form-group input:focus, .form-group select:focus { border-color: #3b82f6; outline: none; }

.divider { margin: 30px 0; border: none; border-top: 1px solid #e5e7eb; }
.section-title { font-size: 1.1rem; color: #111827; margin-bottom: 20px; font-weight: 700; }

.row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.agreement-box { background-color: #f9fafb; padding: 15px; border-radius: 8px; display: flex; gap: 10px; align-items: flex-start; margin-bottom: 30px; }
.agreement-box input { width: 20px; height: 20px; margin-top: 2px; flex-shrink: 0; }
.agreement-box label { font-size: 0.9rem; color: #1f2937; cursor: pointer; }
.agreement-box .desc { display: block; font-size: 0.8rem; color: #6b7280; margin-top: 4px; }
.signup-btn { width: 100%; padding: 14px; background-color: #3b82f6; color: white; border: none; border-radius: 8px; font-size: 1.1rem; font-weight: 700; cursor: pointer; }
.signup-btn:hover { background-color: #2563eb; }
</style>