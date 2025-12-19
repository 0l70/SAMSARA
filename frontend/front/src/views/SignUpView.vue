<template>
  <div class="signup-container">
    <div class="signup-card">
      <h1>회원가입</h1>
      <p class="subtitle">금융 서비스 이용을 위해 정보를 입력해주세요.</p>

      <form @submit.prevent="handleSignup">
        <div class="form-group">
          <label>아이디</label>
          <input type="text" v-model="form.username" required placeholder="아이디 입력">
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

        <h3 class="section-title">📊 맞춤 추천 정보 (필수)</h3>
        
        <div class="row">
          <div class="form-group half">
            <label>나이</label>
            <input type="number" v-model.number="form.age" placeholder="예: 25">
          </div>
          <div class="form-group half">
            <label>연봉 (만원)</label>
            <input type="number" v-model.number="form.salary" placeholder="예: 3000">
          </div>
        </div>

        <div class="form-group">
          <label>보유 자산 (만원)</label>
          <input type="number" v-model.number="form.wealth" placeholder="예: 5000">
        </div>

        <div class="agreement-box">
          <input type="checkbox" id="mydata" v-model="form.is_mydata_agreed">
          <label for="mydata">
            <strong>[선택] 마이데이터 서비스 동의</strong>
            <span class="desc">동의 시 자산 분석을 통한 정밀한 상품 추천이 가능합니다.</span>
          </label>
        </div>

        <button type="submit" class="signup-btn">가입하기</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // 스토어 API URL 사용 권장

const router = useRouter()
const store = useAuthStore()

const form = ref({
  username: '',
  password: '',
  nickname: '',
  age: null,
  salary: null,
  wealth: null,
  is_mydata_agreed: false
})
const passwordConfirm = ref('')

const handleSignup = async () => {
  // 1. 비밀번호 일치 확인
  if (form.value.password !== passwordConfirm.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 2. 필수값 체크
  if (!form.value.age || !form.value.salary || !form.value.wealth) {
    alert('나이, 연봉, 자산 정보는 필수입니다.')
    return
  }

  try {
    // 3. 데이터 포장 (서버가 원하는 이름 password1, password2로 변환)
    const payload = {
      username: form.value.username,
      password1: form.value.password,      // 핵심 수정: password -> password1
      password2: passwordConfirm.value,    // 핵심 수정: 추가됨 -> password2
      nickname: form.value.nickname,
      age: form.value.age,
      salary: form.value.salary,
      wealth: form.value.wealth,
      is_mydata_agreed: form.value.is_mydata_agreed
    }

    // 4. 전송 (payload 사용)
    // store.API_URL이 있다면 사용하고, 없으면 직접 주소 입력
    const url = store.API_URL 
      ? `${store.API_URL}/api/v1/accounts/signup/`
      : 'http://127.0.0.1:8000/api/v1/accounts/signup/'
      
    await axios.post(url, payload)
    
    alert('회원가입이 완료되었습니다!')
    
    // 라우터 이름 소문자 'login'으로 이동
    router.push({ name: 'login' }) 
    
  } catch (error) {
    console.error(error)
    // 에러 메시지 자세히 보여주기
    const msg = error.response?.data 
      ? JSON.stringify(error.response.data) 
      : '정보를 다시 확인해주세요.'
    alert('회원가입 실패: ' + msg)
  }
}
</script>

<style scoped>
/* 전체 컨테이너: 화면 중앙 정렬 */
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 90vh;
  background-color: #f5f7fa;
  padding: 20px;
}

/* 흰색 카드 박스 */
.signup-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 450px; 
}

/* 제목 스타일 */
h1 { margin-bottom: 10px; color: #1f2937; text-align: center; font-size: 2rem; font-weight: 800; }
.subtitle { text-align: center; color: #6b7280; margin-bottom: 30px; font-size: 0.95rem; }

/* 입력 폼 공통 스타일 */
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #374151; font-size: 0.95rem; }

/* 입력창 스타일 */
.form-group input { 
  width: 100%; 
  padding: 12px; 
  border: 1px solid #d1d5db; 
  border-radius: 8px; 
  font-size: 1rem; 
  box-sizing: border-box; 
  transition: border 0.2s; 
}
.form-group input:focus { border-color: #3b82f6; outline: none; box-shadow: 0 0 0 3px rgba(59,130,246,0.1); }

/* 구분선 */
.divider { margin: 30px 0; border: none; border-top: 1px solid #e5e7eb; }
.section-title { font-size: 1.1rem; color: #111827; margin-bottom: 20px; font-weight: 700; }

/* 나이/연봉 한 줄에 배치 */
.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

/* 체크박스 영역 */
.agreement-box { 
  background-color: #eff6ff; padding: 15px; border-radius: 8px; 
  display: flex; gap: 10px; align-items: flex-start; margin-bottom: 30px; 
}
.agreement-box input { width: 20px; height: 20px; margin-top: 2px; flex-shrink: 0; }
.agreement-box label { font-size: 0.9rem; color: #1f2937; cursor: pointer; line-height: 1.4; }
.agreement-box .desc { display: block; font-size: 0.8rem; color: #6b7280; margin-top: 4px; font-weight: normal; }

/* 가입하기 버튼 */
.signup-btn {
  width: 100%; padding: 14px; background-color: #3b82f6; color: white;
  border: none; border-radius: 8px; font-size: 1.1rem; font-weight: 700;
  cursor: pointer; transition: background 0.2s;
}
.signup-btn:hover { background-color: #2563eb; }
</style>