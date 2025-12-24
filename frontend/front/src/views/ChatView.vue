<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>🤖 FinBot</h1>
      <span v-if="userInfo" class="user-badge">
        {{ userInfo.nickname }}님 ({{ mbtiLabel }})
      </span>
    </div>

    <div class="chat-window" ref="chatWindow">
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        :class="['message', msg.role]"
      >
        <div class="bubble">
          <div v-if="msg.role === 'ai'" v-html="renderMarkdown(msg.content)"></div>
          <div v-else>{{ msg.content }}</div>
        </div>
      </div>

      <div v-if="isLoading" class="message ai">
        <div class="bubble loading">
          <span>.</span><span>.</span><span>.</span>
        </div>
      </div>
    </div>

    <div class="input-area">
      <input 
        v-model="userInput" 
        @keyup.enter="sendMessage"
        placeholder="금융 상품이나 고민을 물어보세요..." 
        :disabled="isLoading"
      />
      <button @click="sendMessage" :disabled="isLoading || !userInput.trim()">
        전송
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { marked } from 'marked' // 마크다운 변환기


const router = useRouter()
const store = useAuthStore()

const messages = ref([
  { role: 'ai', content: '안녕하세요! 당신만을 위한 금융 비서 FinBot입니다. 무엇을 도와드릴까요?' }
])
const userInput = ref('')
const isLoading = ref(false)
const chatWindow = ref(null)
const userInfo = ref(null) // 사용자 정보 저장용


// ★ MBTI 변환 사전
const mbtiMap = {
  safe: '성실한 개미 🐜',
  neutral: '신중한 햄스터 🐹',
  active: '똑똑한 여우 🦊',
  aggressive: '용감한 사자 🦁'
}

// ★ 화면 표시용 이름 계산 (없으면 '진단 필요'라고 뜸)
const mbtiLabel = computed(() => {
  if (userInfo.value && userInfo.value.mbti) {
    return mbtiMap[userInfo.value.mbti] || userInfo.value.mbti
  }
  return '성향 미진단'
})

// 마크다운 렌더링 함수
const renderMarkdown = (text) => {
  return marked(text)
}

// 스크롤을 항상 바닥으로
const scrollToBottom = async () => {
  await nextTick()
  if (chatWindow.value) {
    chatWindow.value.scrollTop = chatWindow.value.scrollHeight
  }
}

// 1. 입장 시 사용자 정보 확인 (MBTI 없으면 퇴장)
onMounted(async () => {
  if (!store.token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    const res = await axios.get(`${store.API_URL}/api/v1/accounts/user/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    
    userInfo.value = res.data

    if (!userInfo.value.mbti) {
      alert('맞춤 상담을 위해 금융 성향 테스트를 먼저 진행해주세요! 📝')
      router.push({ name: 'test' })
    }
  } catch (err) {
    console.error(err)
    alert('정보를 불러오는 데 실패했습니다.')
  }
})

// 2. 메시지 전송
const sendMessage = async () => {
  if (!userInput.value.trim()) return

  // 사용자 메시지 추가
  const text = userInput.value
  messages.value.push({ role: 'user', content: text })
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    // ★ 핵심 로직: 마이데이터 동의 여부에 따른 데이터 필터링
    let payloadUserInfo = {};

    if (userInfo.value.is_mydata_agreed) {
      // [동의 함] 진짜 내 정보를 보냄
      payloadUserInfo = {
        age: userInfo.value.age,
        gender: userInfo.value.gender,
        job: userInfo.value.job,
        mbti: userInfo.value.mbti,
        income_source: userInfo.value.income_source
      };
    } else {
      // [동의 안 함] '비공개'라는 마커를 보냄
      payloadUserInfo = {
        age: '정보제공 미동의',
        gender: '정보제공 미동의',
        job: '정보제공 미동의',
        mbti: '정보제공 미동의',
        income_source: '정보제공 미동의'
      };
    }

    // 백엔드로 전송
    const res = await axios.post(`${store.API_URL}/api/v1/chatbot/chat/`, {
      message: text,
      user_info: payloadUserInfo // 위에서 만든 정보 전송
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })

    // AI 응답 추가
    messages.value.push({ role: 'ai', content: res.data.response })
    
  } catch (err) {
    console.error(err)
    messages.value.push({ role: 'ai', content: '죄송해요, 잠시 문제가 생겼어요. 다시 시도해주세요. 😥' })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 600px; margin: 30px auto; border: 1px solid #ddd; border-radius: 16px;
  overflow: hidden; display: flex; flex-direction: column; height: 80vh; background: #fff;
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.chat-header {
  background: #3b82f6; color: white; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center;
}
.chat-header h1 { font-size: 1.2rem; margin: 0; font-weight: 700; }
.user-badge { background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; }

.chat-window {
  flex: 1; padding: 20px; overflow-y: auto; background: #f9fafb; display: flex; flex-direction: column; gap: 15px;
}

.message { display: flex; }
.message.user { justify-content: flex-end; }
.message.ai { justify-content: flex-start; }

.bubble {
  max-width: 70%; padding: 12px 16px; border-radius: 16px; font-size: 0.95rem; line-height: 1.5; word-break: break-word;
}
.message.user .bubble { background: #3b82f6; color: white; border-bottom-right-radius: 2px; }
.message.ai .bubble { background: white; color: #333; border: 1px solid #e5e7eb; border-bottom-left-radius: 2px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }

/* 마크다운 스타일링 (v-html 내부) */
:deep(.bubble ul) { margin: 5px 0 5px 20px; padding: 0; }
:deep(.bubble li) { margin-bottom: 4px; }
:deep(.bubble strong) { color: #2563eb; font-weight: 700; } /* 강조색 */

.input-area {
  padding: 15px; border-top: 1px solid #eee; background: white; display: flex; gap: 10px;
}
.input-area input {
  flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 24px; outline: none; transition: border 0.2s;
}
.input-area input:focus { border-color: #3b82f6; }
.input-area button {
  padding: 0 20px; background: #3b82f6; color: white; border: none; border-radius: 24px; font-weight: 600; cursor: pointer;
}
.input-area button:disabled { background: #9ca3af; cursor: not-allowed; }

/* 로딩 애니메이션 */
.loading span {
  display: inline-block; animation: bounce 1.4s infinite ease-in-out both; margin: 0 2px;
}
.loading span:nth-child(1) { animation-delay: -0.32s; }
.loading span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>