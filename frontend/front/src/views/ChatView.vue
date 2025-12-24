<template>
  <div class="chat-container">
    <div class="chat-header">
      <h1>🤖 FinBot</h1>
      <span v-if="userInfo" class="user-badge">
        {{ userInfo.nickname }}님 ({{ mbtiLabel }})
      </span>
    </div>

    <div class="chat-window" ref="chatWindow">
      <div v-for="(msg, index) in messages" :key="index">
        
        <div v-if="shouldShowDate(index)" class="date-divider">
          <span>{{ formatDate(msg.created_at) }}</span>
        </div>

        <div :class="['message', msg.role]">
          <div v-if="msg.role === 'ai'" class="profile-icon">🤖</div>

          <div class="bubble">
            <div v-if="msg.role === 'ai'" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
            
            <span class="time-stamp">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="message ai">
        <div class="profile-icon">🤖</div>
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
import { marked } from 'marked'

const router = useRouter()
const store = useAuthStore()

// 초기값은 비워둡니다 (DB에서 가져올 거니까)
const messages = ref([]) 
const userInput = ref('')
const isLoading = ref(false)
const chatWindow = ref(null)
const userInfo = ref(null)

const mbtiMap = {
  safe: '성실한 개미 🐜',
  neutral: '신중한 햄스터 🐹',
  active: '똑똑한 여우 🦊',
  aggressive: '용감한 사자 🦁'
}

const mbtiLabel = computed(() => {
  if (userInfo.value && userInfo.value.mbti) {
    return mbtiMap[userInfo.value.mbti] || userInfo.value.mbti
  }
  return '성향 미진단'
})

const renderMarkdown = (text) => marked(text)

const scrollToBottom = async () => {
  await nextTick()
  if (chatWindow.value) {
    chatWindow.value.scrollTop = chatWindow.value.scrollHeight
  }
}

// 📅 날짜 포맷팅 (2024년 12월 25일)
const formatDate = (dateString) => {
  if (!dateString) return '오늘' // 방금 보낸 메시지 등
  const date = new Date(dateString)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

// 🕒 시간 포맷팅 (오후 3:40)
const formatTime = (dateString) => {
  if (!dateString) return new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
  return new Date(dateString).toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}

// 날짜 구분선 표시 로직
const shouldShowDate = (index) => {
  // 첫 번째 메시지는 무조건 날짜 표시
  if (index === 0) return true
  
  const currentMsgDate = messages.value[index].created_at
  const prevMsgDate = messages.value[index - 1].created_at

  // 날짜 정보가 없으면 패스
  if (!currentMsgDate || !prevMsgDate) return false

  // 날짜(일)가 달라졌으면 true
  const curr = new Date(currentMsgDate).toDateString()
  const prev = new Date(prevMsgDate).toDateString()
  return curr !== prev
}

onMounted(async () => {
  if (!store.token) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    // 1. 사용자 정보 가져오기
    const userRes = await axios.get(`${store.API_URL}/api/v1/accounts/user/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    userInfo.value = userRes.data
    
    if (!userInfo.value.mbti) {
      alert('맞춤 상담을 위해 금융 성향 테스트를 먼저 진행해주세요! 📝')
      router.push({ name: 'test' })
      return
    }

    // 2. ★ 대화 내역(History) DB에서 가져오기
    const historyRes = await axios.get(`${store.API_URL}/api/v1/chatbot/history/`, {
      headers: { Authorization: `Token ${store.token}` }
    })

    if (historyRes.data.length > 0) {
      messages.value = historyRes.data
    } else {
      // 대화 내역이 없으면 기본 환영 메시지 (DB 저장 안 함, 화면에만 표시)
      messages.value = [{ 
        role: 'ai', 
        content: '안녕하세요! 당신만을 위한 금융 비서 FinBot입니다. 무엇을 도와드릴까요?',
        created_at: new Date().toISOString()
      }]
    }
    
    // 로딩 후 스크롤 내리기
    scrollToBottom()

  } catch (err) {
    console.error(err)
    alert('정보를 불러오는 데 실패했습니다.')
  }
})

const sendMessage = async () => {
  if (!userInput.value.trim()) return

  const text = userInput.value
  
  // 내 메시지 화면에 즉시 추가 (created_at은 현재 시간으로 임시 표시)
  messages.value.push({ 
    role: 'user', 
    content: text,
    created_at: new Date().toISOString() 
  })
  
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    // 마이데이터 동의 여부 payload 생성
    let payloadUserInfo = {}
    if (userInfo.value.is_mydata_agreed) {
      payloadUserInfo = {
        age: userInfo.value.age,
        gender: userInfo.value.gender,
        job: userInfo.value.job,
        mbti: userInfo.value.mbti,
        income_source: userInfo.value.income_source
      }
    } else {
      payloadUserInfo = {
        age: '정보제공 미동의',
        gender: '정보제공 미동의',
        job: '정보제공 미동의',
        mbti: '정보제공 미동의',
        income_source: '정보제공 미동의'
      }
    }

    // ★ 수정됨: history 배열을 보내지 않음 (백엔드가 DB에서 확인)
    const res = await axios.post(`${store.API_URL}/api/v1/chatbot/chat/`, {
      message: text,
      user_info: payloadUserInfo
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })

    // AI 응답 추가 (백엔드에서 오는 데이터 형식이 바뀌었을 수 있으니 확인)
    messages.value.push({ 
      role: 'ai', 
      content: res.data.response,
      created_at: new Date().toISOString() 
    })
    
  } catch (err) {
    console.error(err)
    messages.value.push({ 
      role: 'ai', 
      content: '죄송해요, 잠시 문제가 생겼어요. 다시 시도해주세요. 😥',
      created_at: new Date().toISOString() 
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 600px; margin: 30px auto; 
  border: 1px solid var(--border-color); /* #ddd -> 변수 */
  border-radius: 16px;
  overflow: hidden; display: flex; flex-direction: column; height: 80vh; 
  background: var(--bg-card); /* #fff -> 변수 */
  box-shadow: 0 10px 20px var(--shadow-color);
  transition: background-color 0.3s ease;
}

/* =====================
  2. 헤더 섹션
===================== */
.chat-header {
  background: #3b82f6; color: white; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center;
}
.chat-header h1 { font-size: 1.2rem; margin: 0; font-weight: 700; }
.user-badge { background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-size: 0.85rem; }

/* =====================
  3. 채팅 창 및 메시지 버블
===================== */
.chat-window {
  flex: 1; padding: 20px; overflow-y: auto; 
  background: var(--bg-body); /* #f9fafb -> 변수 */
  display: flex; flex-direction: column; gap: 15px;
}

/* 프로필 아이콘 스타일 */
.profile-icon {
  width: 36px; height: 36px; background: #e0e7ff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-right: 8px; flex-shrink: 0;
}

.message { display: flex; align-items: flex-start; margin-bottom: 5px;}
.message.user { justify-content: flex-end; }
.message.ai { justify-content: flex-start; }

.bubble {
  max-width: 75%; padding: 12px 16px; border-radius: 16px; font-size: 0.95rem; line-height: 1.5; word-break: break-word; position: relative;
}

/* 사용자 메시지 (블루 톤 유지) */
.message.user .bubble { background: #3b82f6; color: white; border-bottom-right-radius: 2px; }

/* AI 메시지 (다크모드 대응) */
.message.ai .bubble { 
  background: var(--bg-card); /* white -> 변수 */
  color: var(--text-primary); /* #333 -> 변수 */
  border: 1px solid var(--border-color); 
  border-bottom-left-radius: 2px; 
  box-shadow: 0 2px 4px var(--shadow-color); 
}

/* 마크다운 스타일링 (v-html 내부) */
:deep(.bubble ul) { margin: 5px 0 5px 20px; padding: 0; }
:deep(.bubble li) { margin-bottom: 4px; }
:deep(.bubble strong) { color: #2563eb; font-weight: 700; } /* 강조색 */

/* =====================
  4. 하단 입력 영역
===================== */
.input-area {
  padding: 15px; border-top: 1px solid var(--border-color); 
  background: var(--bg-card); /* white -> 변수 */
  display: flex; gap: 10px;
}

.input-area input {
  flex: 1; padding: 12px; 
  border: 1px solid var(--border-color); /* #ddd -> 변수 */
  border-radius: 24px; outline: none; transition: all 0.2s;
  background-color: var(--bg-body); /* 입력창 내부 어둡게 */
  color: var(--text-primary);
}

.input-area input:focus { 
  border-color: #3b82f6; 
  background-color: var(--bg-card); /* 포커스 시 약간 밝아짐 */
}

.input-area button {
  padding: 0 20px; background: #3b82f6; color: white; border: none; border-radius: 24px; font-weight: 600; cursor: pointer;
}
.input-area button:disabled { background: var(--text-muted); cursor: not-allowed; opacity: 0.6; }

/* 로딩 애니메이션 (색상 변수화) */
.loading span {
  display: inline-block; animation: bounce 1.4s infinite ease-in-out both; margin: 0 2px;
  background-color: var(--text-muted); /* 로딩 점 색상 */
  width: 6px; height: 6px; border-radius: 50%; /* 로딩바 형태 유지 */
}
.loading span:nth-child(1) { animation-delay: -0.32s; }
.loading span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>