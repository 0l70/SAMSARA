import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  
  // 1. State (상태)
  const token = ref(localStorage.getItem('token') || null) // 새로고침해도 유지되게
  const nickname = ref(localStorage.getItem('nickname') || null) // 닉네임도 저장
  const API_URL = 'http://127.0.0.1:8000'

  // 2. Getters (계산된 값)
  const isLogin = computed(() => !!token.value) // 토큰이 있으면 로그인 상태

  // 3. Actions (기능)
  
  // [핵심] 로그인 기능
  const logIn = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/accounts/login/`,
      data: payload,
    })
      .then((res) => {
        // (1) 토큰 저장
        const newToken = res.data.key
        token.value = newToken
        localStorage.setItem('token', newToken)

        // (2) 로그인 성공했으니, 바로 내 정보(닉네임) 가져오기 실행!
        // dj-rest-auth 기본 설정이면 로그인 응답에 user 정보가 없을 수 있음
        // 그래서 토큰을 가지고 /user/ 정보를 요청해야 함.
        fetchCurrentUser(newToken)

        router.push({ name: 'articles' }) // 메인으로 이동
      })
      .catch((err) => {
        console.log(err)
        alert('아이디 또는 비밀번호를 확인하세요.')
      })
  }

  // [추가됨] 내 정보(닉네임) 가져오는 함수
  const fetchCurrentUser = (tokenValue) => {
    axios({
      method: 'get',
      // dj-rest-auth 기본 유저 정보 URL (프로젝트마다 다를 수 있음, 확인 필요)
      // 보통: /api/v1/accounts/user/ 또는 /accounts/user/
      url: `${API_URL}/api/v1/accounts/user/`, 
      headers: {
        Authorization: `Token ${tokenValue}` // 토큰을 헤더에 실어서 보냄
      }
    })
    .then((res) => {
      console.log('유저 정보 가져오기 성공:', res.data)
      
      // 서버에서 받은 닉네임 저장 (없으면 username으로 대체)
      const userNickname = res.data.nickname || res.data.username || '회원'
      nickname.value = userNickname
      localStorage.setItem('nickname', userNickname)
    })
    .catch((err) => {
      console.log('유저 정보 가져오기 실패:', err)
    })
  }

  // 로그아웃
  const logOut = function () {
    token.value = null
    nickname.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('nickname')
    router.push({ name: 'login' })
  }

  return { 
    token, 
    nickname, 
    API_URL, 
    isLogin, 
    logIn, 
    logOut,
    fetchCurrentUser 
  }
}, { persist: true }) // persist 플러그인 쓰고 있다면 유지됨