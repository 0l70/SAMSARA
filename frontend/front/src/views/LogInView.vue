<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1>로그인</h1>
      
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="username">아이디</label>
          <input 
            type="text" 
            id="username" 
            name="username" 
            v-model.trim="username" 
            placeholder="아이디를 입력하세요"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">비밀번호</label>
          <input 
            type="password" 
            id="password" 
            name="password" 
            v-model.trim="password" 
            placeholder="비밀번호를 입력하세요"
            required
          >
        </div>

        <button type="submit" class="btn-submit">로그인</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router' // 1. 라우터 import 추가

const store = useAuthStore()
const router = useRouter() // 2. 라우터 사용 설정
const username = ref(null)
const password = ref(null)

// 3. 함수 앞에 async 붙이기
const submitForm = async function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  
  try {
    // 4. 스토어의 로그인이 끝날 때까지 기다림 (await)
    await store.logIn(payload)
    
    // 5. 로그인 성공 시 홈으로 이동 (replace는 뒤로가기 눌러도 로그인창 안 나오게 함)
    router.replace({ name: 'home' }) 
  } catch (err) {
    // 실패 시 스토어에서 이미 alert를 띄웠으므로 여기선 따로 할 게 없거나,
    // 추가적인 에러 처리를 할 수 있음 (예: 비밀번호 입력창 비우기)
    password.value = '' 
  }
}
</script>

<style scoped>
/* 전체 화면 중앙 정렬을 위한 래퍼 */
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh; /* 화면 높이의 80% 정도 차지하게 */
  background-color: #f8f9fa; /* 아주 연한 회색 배경 */
}

/* 로그인 카드 디자인 */
.auth-card {
  width: 100%;
  max-width: 400px; /* 너무 넓어지지 않게 제한 */
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

/* 폼 요소 간격 */
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #555;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
  transition: border-color 0.3s;
}

/* 입력창 클릭했을 때 초록색 테두리 */
input:focus {
  border-color: #42b983;
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

/* 로그인 버튼 */
.btn-submit {
  width: 100%;
  padding: 14px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #3aa876; /* 호버 시 약간 진하게 */
}
</style>