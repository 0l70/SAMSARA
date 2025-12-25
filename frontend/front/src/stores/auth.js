import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000'

  const token = ref(localStorage.getItem('token'))
  const username = ref(localStorage.getItem('username'))
  const nickname = ref(localStorage.getItem('nickname'))
  
  // ★ [추가 1] MBTI 상태 변수 추가 (새로고침 해도 유지되게 localStorage에서 읽기)
  const mbti = ref(localStorage.getItem('mbti'))

  const isLogin = computed(() => !!token.value)

  // 1. 로그인 기능
  const logIn = async function (payload) {
    const { username: inputUsername, password } = payload

    try {
      const res = await axios.post(`${API_URL}/api/v1/accounts/login/`, {
        username: inputUsername,
        password: password
      })

      const newToken = res.data.key
      
      // 토큰과 아이디 저장
      token.value = newToken
      username.value = inputUsername
      localStorage.setItem('token', newToken)
      localStorage.setItem('username', inputUsername)

      // 닉네임 & MBTI 가져오기
      await fetchCurrentUser(newToken)

    } catch (err) {
      console.log(err)
      alert('아이디 또는 비밀번호를 확인해주세요.')
      throw err 
    }
  }

  // 2. 내 정보 가져오기 기능
  const fetchCurrentUser = async (tokenValue) => {
    try {
      const res = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/accounts/user/`, 
        headers: {
          Authorization: `Token ${tokenValue}`
        }
      })
      
      console.log('유저 정보 가져오기 성공:', res.data)
      
      const userNickname = res.data.nickname || res.data.username
      // ★ [추가 2] 백엔드에서 받은 MBTI 정보를 저장
      const userMbti = res.data.mbti 
      
      nickname.value = userNickname
      mbti.value = userMbti // Pinia 상태 업데이트

      localStorage.setItem('nickname', userNickname)
      // ★ [추가 3] 로컬 스토리지에도 저장
      if (userMbti) {
        localStorage.setItem('mbti', userMbti)
      }

    } catch (err) {
      console.log('유저 정보 로드 실패:', err)
    }
  }

  const logOut = function () {
    token.value = null
    username.value = null
    nickname.value = null
    // ★ [추가 4] 로그아웃 시 MBTI 초기화
    mbti.value = null

    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('nickname')
    localStorage.removeItem('mbti') // 로컬스토리지 삭제
    
    alert('로그아웃 되었습니다.')
    router.push({ name: 'home' })
  }

  return { 
    token, username, nickname, 
    mbti, // ★ [추가 5] 밖에서 쓸 수 있게 return에 포함
    API_URL, isLogin, 
    logIn, logOut, fetchCurrentUser 
  }
}, { persist: true })