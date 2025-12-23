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

  const isLogin = computed(() => !!token.value)

  // 1. 로그인 기능
  const logIn = function (payload) {
    const { username: inputUsername, password } = payload

    axios.post(`${API_URL}/api/v1/accounts/login/`, {
      username: inputUsername,
      password: password
    })
      .then((res) => {
        const newToken = res.data.key
        
        // 일단 토큰과 아이디 저장
        token.value = newToken
        username.value = inputUsername
        localStorage.setItem('token', newToken)
        localStorage.setItem('username', inputUsername)

        // 👇 [핵심] 로그인 성공했으니, 바로 서버에 닉네임을 물어봅니다!
        fetchCurrentUser(newToken)

        router.push({ name: 'home' })
      })
      .catch((err) => {
        console.log(err)
        alert('아이디 또는 비밀번호를 확인해주세요.')
      })
  }

  // 2. 내 정보(닉네임) 가져오기 기능
  const fetchCurrentUser = (tokenValue) => {
    axios({
      method: 'get',
      // 👇 백엔드 URL이 '/accounts/user/' 인지 확인 필요!
      url: `${API_URL}/api/v1/accounts/user/`, 
      headers: {
        Authorization: `Token ${tokenValue}`
      }
    })
    .then((res) => {
      console.log('유저 정보 가져오기 성공:', res.data)
      
      // 백엔드에서 보내준 데이터 중 nickname을 찾습니다.
      // (만약 닉네임이 없으면 username을 대신 씁니다)
      const userNickname = res.data.nickname || res.data.username
      
      nickname.value = userNickname
      localStorage.setItem('nickname', userNickname)
    })
    .catch((err) => {
      console.log('유저 정보 로드 실패:', err)
    })
  }

  const logOut = function () {
    token.value = null
    username.value = null
    nickname.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('nickname')
    
    alert('로그아웃 되었습니다.')
    router.push({ name: 'home' })
  }

  return { 
    token, username, nickname, 
    API_URL, isLogin, 
    logIn, logOut, fetchCurrentUser 
  }
}, { persist: true })