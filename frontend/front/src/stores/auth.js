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

  // 1. 로그인 기능 (수정됨!)
  // ★ async를 붙여서 비동기 함수로 만듭니다.
  const logIn = async function (payload) {
    const { username: inputUsername, password } = payload

    try {
      // ★ await를 붙여서 응답이 올 때까지 기다립니다.
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

      // 닉네임 가져오기도 기다렸다가 완료합니다.
      await fetchCurrentUser(newToken)

      // ★ [삭제] router.push({ name: 'home' }) 
      // 이유: 회원가입 후에는 'chatbot'으로 가야 하고, 일반 로그인은 'home'으로 가야 합니다.
      // 어디로 갈지는 이 함수를 부르는 컴포넌트(Vue 파일)가 결정하게 둡니다.

    } catch (err) {
      console.log(err)
      alert('아이디 또는 비밀번호를 확인해주세요.')
      // ★ 에러를 던져서 컴포넌트(SignUpView)가 로그인 실패를 알 수 있게 합니다.
      throw err 
    }
  }

  // 2. 내 정보(닉네임) 가져오기 기능 (수정됨)
  // 여기도 async/await로 맞추는 게 좋습니다.
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
      
      nickname.value = userNickname
      localStorage.setItem('nickname', userNickname)
    } catch (err) {
      console.log('유저 정보 로드 실패:', err)
    }
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