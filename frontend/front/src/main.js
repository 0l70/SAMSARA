import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' // ★ 1. 플러그인 가져오기

import App from './App.vue'
import router from './router'

// CSS 파일이 있다면 보통 여기서 import 합니다 (예: import './assets/main.css')

const app = createApp(App)
const pinia = createPinia()

// pinia에 플러그인 등록 (이게 있어야 persist: true가 작동함)
pinia.use(piniaPluginPersistedstate)

app.use(pinia) // 플러그인이 장착된 pinia를 앱에 연결
app.use(router)

app.mount('#app')