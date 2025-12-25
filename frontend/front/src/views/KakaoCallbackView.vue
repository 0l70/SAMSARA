<template>
  <div class="callback-container">
    <div class="loader"></div>
    <div class="message">
      <h3>로그인 중입니다... 🦁</h3>
      <p>잠시만 기다려주세요.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

onMounted(async () => {
  const code = route.query.code // 1. URL 뒤에 붙은 인가 코드(?code=...) 가져오기
  
  if (code) {
    try {
      // 2. 백엔드로 코드 쏘기
      const res = await axios.post(`${store.API_URL}/api/v1/accounts/kakao/`, {
        code: code
      })
      
      // 3. 백엔드에서 받은 정보 (토큰 + 유저정보)
      const { key, username, nickname, age, mbti } = res.data

      // 4. Pinia & 로컬스토리지 저장 (수동 로그인 처리)
      localStorage.setItem('token', key)
      localStorage.setItem('username', username)
      localStorage.setItem('nickname', nickname)
      if (mbti) localStorage.setItem('mbti', mbti)
      
      store.token = key
      store.username = username
      store.nickname = nickname
      store.mbti = mbti

      // 5. ★ [분기 처리] 신규 가입자(정보 없음) vs 기존 회원
      if (age === 0) {
        // 나이가 0이다 = 모델 default 값이다 = 추가 정보 입력 안 했다.
        const confirmMsg = confirm(`환영합니다, ${nickname}님! 🎉\n금융 상품 추천을 위해 나이와 직업 정보가 필요합니다.\n입력하러 가시겠습니까?`)
        
        if (confirmMsg) {
          router.replace({ name: 'mypage' }) // 정보 수정 페이지로 이동
        } else {
          router.replace({ name: 'home' })
        }
      } else {
        // 이미 정보가 있는 회원
        alert(`돌아오셨군요, ${nickname}님! 😎`)
        router.replace({ name: 'home' })
      }

    } catch (err) {
      console.error(err)
      alert('로그인에 실패했습니다. 다시 시도해주세요.')
      router.replace({ name: 'login' }) // 실패 시 로그인 페이지로
    }
  }
})
</script>

<style scoped>
.callback-container {
  height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #FEE500; /* 카카오 노란색 */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>