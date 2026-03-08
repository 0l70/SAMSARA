import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// pinia 플러그인 등록
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

// ========================================================
// ★ [추가] 카카오 SDK 초기화 코드
// ========================================================
// .env 파일에서 내 키 가져오기
const { VITE_KAKAO_JS_KEY } = import.meta.env

// 카카오 객체가 로드되었는지 확인 후 초기화
// (이 코드가 없으면 "Uncaught TypeError"가 또 날 수 있음)
if (window.Kakao && !window.Kakao.isInitialized()) {
    try {
        window.Kakao.init(VITE_KAKAO_JS_KEY)
        console.log('✅ 카카오 로그인 SDK 초기화 성공!')
    } catch (e) {
        console.error('❌ 카카오 SDK 초기화 실패:', e)
    }
}
// ========================================================

app.mount('#app')