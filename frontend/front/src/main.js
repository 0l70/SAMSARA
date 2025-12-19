import { createApp } from 'vue'
import { createPinia } from 'pinia' // 이 줄이 있어야 함
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia()) // 이 줄이 반드시 있어야 함!
app.use(router)

app.mount('#app')
