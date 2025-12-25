<template>
  <div class="page-overlay">
    <div class="ios-frame" :class="{ dark: isDarkMode }">
      
      <header class="ios-header">
        <button class="back-btn" @click="router.go(-1)">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 19L8 12L15 5"/>
          </svg>
        </button>
        
        <div class="header-center">
          <div class="bot-name">FinBot</div>
          <div class="bot-status">금융 비서</div>
        </div>

        <div class="header-right-info" v-if="userInfo">
          <span class="user-badge">
            {{ userInfo.nickname || '회원' }}
            <span v-if="userInfo.mbti">({{ userInfo.mbti }})</span>
          </span>
        </div>
      </header>

      <main class="chat-container" ref="chatWindow" @click="handleLinkClick">
        <div class="messages-wrapper">
          <div v-for="(msg, index) in messages" :key="index" :class="['message-row', msg.role]">
            
            <div v-if="shouldShowDate(index)" class="date-divider-container">
              <span class="date-divider">{{ formatDate(msg.created_at) }}</span>
            </div>

            <div class="bubble-group">
              <div v-if="msg.role === 'ai'" class="bot-avatar-container">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="2" y="6" width="20" height="14" rx="4" fill="white" fill-opacity="0.9"/>
                  <path d="M7 11H9M15 11H17" stroke="#4F46E5" stroke-width="2" stroke-linecap="round"/>
                  <path d="M12 2V6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="12" cy="2" r="2" fill="white"/>
                </svg>
              </div>

              <div class="message-bubble">
                <div v-if="msg.role === 'ai'" class="markdown-body" v-html="renderMessage(msg.content)"></div>
                <div v-else>{{ msg.content }}</div>
              </div>
            </div>

            <span class="timestamp">{{ formatTime(msg.created_at) }}</span>
          </div>

          <div v-if="isLoading" class="message-row ai">
            <div class="bubble-group">
              <div class="bot-avatar-container">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="2" y="6" width="20" height="14" rx="4" fill="white" fill-opacity="0.9"/>
                  <path d="M7 11H9M15 11H17" stroke="#4F46E5" stroke-width="2" stroke-linecap="round"/>
                  <path d="M12 2V6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="12" cy="2" r="2" fill="white"/>
                </svg>
              </div>

              <div class="message-bubble typing-indicator-bubble">
                <div class="typing-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer class="input-area">
        <div class="input-container">
          <input 
            v-model="userInput" 
            type="text" 
            placeholder="FinBot에게 물어보세요"
            @keyup.enter="sendMessage"
            :disabled="isLoading"
          />
          <button 
            class="send-btn" 
            @click="sendMessage" 
            :disabled="!userInput.trim() || isLoading"
          >
            <svg viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="12" :fill="userInput.trim() ? '#007AFF' : '#C7C7CC'"/>
              <path d="M12 8L12 16M12 8L8 12M12 8L16 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFinanceStore } from '@/stores/finance'
import { marked } from 'marked'

const router = useRouter()
const store = useAuthStore()
const financeStore = useFinanceStore()

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const chatWindow = ref(null)
const userInfo = ref(null)
const isDarkMode = ref(false)

// ------------------------------------------------------------------
// 1. 하이퍼링크 생성 (KB 특★한 적금 해결 로직)
// ------------------------------------------------------------------
const renderMessage = (text) => {
  let html = marked(text)

  const allProducts = [
    ...(financeStore.products || []),
    ...(financeStore.depositProducts || []),
    ...(financeStore.savingProducts || [])
  ]

  // 중복 제거
  const uniqueProducts = Array.from(new Map(allProducts.map(item => [item.fin_prdt_cd, item])).values())
  if (uniqueProducts.length === 0) return html

  // 이름 긴 순서로 정렬 (오매칭 방지)
  const sortedProducts = uniqueProducts.sort((a, b) => b.fin_prdt_nm.length - a.fin_prdt_nm.length)

  sortedProducts.forEach(product => {
    // 1. DB 이름 정제: 괄호 내용 삭제, 특수문자 삭제 -> 순수 한글/영문/숫자만 남김
    const cleanDbName = product.fin_prdt_nm
      .replace(/\n/g, '')
      .replace(/\(.*\)/g, '') // 괄호 안의 내용((정기예금) 등)을 제거하고 매칭
      .replace(/[^가-힣a-zA-Z0-9]/g, '')

    if (cleanDbName.length < 2) return

    // 2. 패턴 생성 (★ 핵심 수정 구간 ★)
    // 기존: .join('[^<]*?') -> 모든 문자 허용 (오류 원인)
    // 수정: .join('[^가-힣a-zA-Z0-9<]*?') -> 글자 사이에는 '공백'이나 '특수문자'만 허용하고, 다른 텍스트가 끼어들면 매칭 실패 처리
    const pattern = cleanDbName.split('').map(c => {
      return c.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    }).join('[^가-힣a-zA-Z0-9<]*?') 

    try {
      // HTML 태그 내부가 아닌 텍스트만 매칭
      const regex = new RegExp(`(${pattern})(?![^<]*>)`, 'gi')
      
      html = html.replace(regex, (match) => {
        // 이미 링크가 걸려있거나 태그 내부인 경우 제외
        if (match.includes('product-link') || match.includes('</a>')) return match
        return `<span class="product-link" data-id="${product.fin_prdt_cd}">${match}</span>`
      })
    } catch (e) {}
  })

  return html
}

const handleLinkClick = (e) => {
  const target = e.target.closest('.product-link')
  if (target) {
    router.push({ name: 'product-detail', params: { id: target.dataset.id } })
  }
}

// ------------------------------------------------------------------
// 2. 다크모드 및 데이터 로드
// ------------------------------------------------------------------
let observer = null
let mediaQuery = null

// ... import 문 등 상단 생략 ...

onMounted(async () => {
  if (!store.token) return router.push({ name: 'login' })

  // (1) 다크모드 감지
  const updateTheme = () => {
    const htmlTheme = document.documentElement.getAttribute('data-theme')
    const sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDarkMode.value = htmlTheme === 'dark' || (!htmlTheme && sysDark)
  }
  updateTheme()
  
  observer = new MutationObserver(updateTheme)
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] })
  mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery.addEventListener('change', updateTheme)

  // (2) 상품 데이터 로드
  if (financeStore.products.length === 0) {
    await financeStore.getProducts()
  }

  // (3) 유저 및 채팅 기록 로드
  try {
    // 유저 정보 가져오기
    const userRes = await axios.get(`${store.API_URL}/api/v1/accounts/user/`, { 
      headers: { Authorization: `Token ${store.token}` } 
    })
    userInfo.value = userRes.data

    // 채팅 기록 가져오기
    const historyRes = await axios.get(`${store.API_URL}/api/v1/chatbot/history/`, { 
      headers: { Authorization: `Token ${store.token}` } 
    })
    
    // ▼▼▼ [핵심 수정] 동의 여부에 따른 첫 인사말 분기 처리 ▼▼▼
    if (historyRes.data.length > 0) {
      messages.value = historyRes.data
    } else {
      let welcomeMsg = ''
      
      if (userInfo.value.is_mydata_agreed) {
        // [True] 동의 상태: 바로 맞춤 추천 시작 멘트
        welcomeMsg = `안녕하세요 ${userInfo.value.nickname}님! \n\n마이데이터 연동이 확인되었습니다. 🙆🏻‍♂️\n**${userInfo.value.mbti || '고객'}**님의 투자 성향과 자산 정보를 바탕으로, 딱 맞는 예적금/펀드 상품을 바로 추천해드릴 수 있어요.\n\n무엇을 찾아드릴까요?`
      } else {
        // [False] 미동의 상태: 동의 권유 멘트
        welcomeMsg = `안녕하세요 ${userInfo.value.nickname}님! FinBot입니다. 🤖\n\n현재 **마이데이터 미동의** 상태라 일반적인 인기 상품 위주로만 추천해드릴 수 있어요.\n\n더 정확한 맞춤 추천과 수익률 계산을 원하시면 마이데이터 제공에 동의해주세요.`
      }

      messages.value = [{ role: 'ai', content: welcomeMsg, created_at: new Date() }]
    }
    // ▲▲▲ [수정 끝] ▲▲▲

    scrollToBottom()
  } catch (err) { console.error(err) }
})

onUnmounted(() => {
  if (observer) observer.disconnect()
  if (mediaQuery) mediaQuery.removeEventListener('change', () => {})
})

// ------------------------------------------------------------------
// 3. 메시지 전송 로직
// ------------------------------------------------------------------
const sendMessage = async () => {
  if (!userInput.value.trim()) return
  const text = userInput.value
  messages.value.push({ role: 'user', content: text, created_at: new Date() })
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    let info = {}
    if (userInfo.value?.is_mydata_agreed) {
      info = { 
        age: userInfo.value.age, 
        gender: userInfo.value.gender, 
        job: userInfo.value.job, 
        mbti: userInfo.value.mbti, 
        income_source: userInfo.value.income_source,
        wealth: userInfo.value.wealth 
      }
    }
    const res = await axios.post(`${store.API_URL}/api/v1/chatbot/chat/`, { message: text, user_info: info }, { headers: { Authorization: `Token ${store.token}` } })
    messages.value.push({ role: 'ai', content: res.data.response, created_at: new Date() })
  } catch (err) {
    messages.value.push({ role: 'ai', content: '죄송합니다. 오류가 발생했습니다.', created_at: new Date() })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

const scrollToBottom = async () => { await nextTick(); if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight }
const formatDate = (d) => new Date(d).toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'short' })
const formatTime = (d) => new Date(d).toLocaleTimeString('ko-KR', { hour: 'numeric', minute: '2-digit' })
const shouldShowDate = (idx) => idx === 0 || new Date(messages.value[idx].created_at).toDateString() !== new Date(messages.value[idx-1].created_at).toDateString()
</script>

<style scoped>
/* ----------------------------------------------------
   Layout Adjustments (Center & Size)
---------------------------------------------------- */
.page-overlay {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 5vh;
  min-height: 100vh;
  background-color: transparent;
  box-sizing: border-box;
}

.ios-frame {
  width: 100%;
  max-width: 600px;
  height: 80vh;
  max-height: 850px;
  background-color: #FFFFFF;
  border-radius: 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
  border: 1px solid #E5E5EA;
  transition: background-color 0.3s, border-color 0.3s;
}

/* ----------------------------------------------------
   Header
---------------------------------------------------- */
.ios-header {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0,0,0,0.1);
  z-index: 10;
  flex-shrink: 0;
}
.back-btn {
  display: flex;
  align-items: center;
  border: none;
  background: none;
  color: #007AFF;
  font-size: 16px;
  cursor: pointer;
  padding: 0;
  width: 60px;
}
.header-center { 
  display: flex; flex-direction: column; align-items: center; flex: 1; 
}
.bot-name { font-weight: 600; font-size: 16px; color: #000; }
.bot-status { font-size: 11px; color: #8E8E93; }

.header-right-info {
  width: 60px;
  display: flex;
  justify-content: flex-end;
}
.user-badge {
  font-size: 11px;
  color: #8E8E93;
  font-weight: 500;
  text-align: right;
  line-height: 1.2;
}

/* ----------------------------------------------------
   Chat Area
---------------------------------------------------- */
.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 16px;
  background-color: #FFFFFF;
}

/* 스크롤바 디자인 (중복 제거됨) */
.chat-container::-webkit-scrollbar { width: 8px; }
.chat-container::-webkit-scrollbar-thumb { background-color: rgba(0, 0, 0, 0.25); border-radius: 4px; }
.chat-container::-webkit-scrollbar-thumb:hover { background-color: rgba(0, 0, 0, 0.4); }
.chat-container::-webkit-scrollbar-track { background-color: transparent; }

.messages-wrapper { display: flex; flex-direction: column; gap: 6px; }

.message-row { display: flex; flex-direction: column; width: 100%; margin-bottom: 8px; }
.message-row.ai { align-items: flex-start; }
.message-row.user { align-items: flex-end; }

/* 날짜 구분선 */
.date-divider-container {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 16px 0;
}
.date-divider {
  background-color: rgba(0,0,0,0.05);
  color: #8E8E93;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 12px;
}

/* Bubbles */
.bubble-group { display: flex; align-items: flex-end; gap: 8px; max-width: 80%; }
.message-row.user .bubble-group { flex-direction: row-reverse; }

.message-bubble {
  padding: 10px 14px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 1.45;
  position: relative;
  word-break: break-word;
}
.message-row.ai .message-bubble { background-color: #E9E9EB; color: #000; border-bottom-left-radius: 4px; }
.message-row.user .message-bubble { background-color: #007AFF; color: #FFF; border-bottom-right-radius: 4px; }

.profile-icon { font-size: 20px; padding-bottom: 4px; }
.timestamp { font-size: 10px; color: #8E8E93; margin-top: 4px; padding: 0 4px; }
.message-row.user .timestamp { text-align: right; }

/* ----------------------------------------------------
   Input Area
---------------------------------------------------- */
.input-area {
  padding: 10px 16px 20px 16px;
  background-color: #F2F2F7;
  border-top: 1px solid rgba(0,0,0,0.1);
  flex-shrink: 0;
}
.input-container {
  display: flex;
  align-items: center;
  background-color: #FFFFFF;
  border-radius: 20px;
  padding: 4px 6px 4px 16px;
  border: 1px solid #C7C7CC;
}
input {
  flex: 1;
  border: none;
  background: none;
  font-size: 16px;
  outline: none;
  padding: 8px 0;
  color: #000;
}
.send-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
}
.send-btn svg { width: 28px; height: 28px; }
/* =========================================
   세련된 봇 아이콘 스타일 (공통 사용)
   ========================================= */
.bot-avatar-container {
  width: 36px;
  height: 36px;
  /* 금융/IT 느낌의 그라데이션 배경 */
  background: linear-gradient(135deg, #4A86E8 0%, #7B61FF 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(74, 134, 232, 0.3);
  margin-bottom: 2px; /* 말풍선 하단 라인과 정렬 */
}

.bot-avatar-container svg {
  width: 20px;
  height: 20px;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

/* 다크모드 대응 */
.ios-frame.dark .bot-avatar-container {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  opacity: 0.9;
}


/* =========================================
   부드러운 타이핑 인디케이터 스타일
   ========================================= */
.typing-indicator-bubble {
  /* 말풍선 높이 고정 및 정렬 */
  height: 40px; 
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px !important; /* 패딩 재조정 */
  min-width: 50px;
}

.typing-dots {
  display: flex;
  gap: 4px;
  padding-top: 2px;
}

.typing-dots span {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #B0B0B5; /* 기본 점 색상 (회색) */
  border-radius: 50%;
  animation: smooth-bounce 1.4s infinite ease-in-out both;
}

/* 다크모드 점 색상 */
.ios-frame.dark .typing-dots span {
  background-color: #636366; 
}

/* 웨이브 애니메이션 */
.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes smooth-bounce {
  0%, 80%, 100% { 
    transform: scale(0.6);
    opacity: 0.5;
  } 
  40% { 
    transform: scale(1);
    opacity: 1;
  }
}
/* Loading */
.typing-indicator span {
  display: inline-block; width: 6px; height: 6px; background-color: #8E8E93; border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both; margin: 0 1px;
}
.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }

/* ----------------------------------------------------
   🌑 DARK MODE
---------------------------------------------------- */
.ios-frame.dark { background-color: #000000; border-color: #333; }

/* Header */
.ios-frame.dark .ios-header { background: rgba(30, 30, 30, 0.9); border-bottom: 1px solid #38383A; }
.ios-frame.dark .bot-name { color: #FFF; }
.ios-frame.dark .back-btn { color: #0A84FF; }

/* Chat Area */
.ios-frame.dark .chat-container { background-color: #000000; }
.ios-frame.dark .message-row.ai .message-bubble { background-color: #262628; color: #FFF; }
.ios-frame.dark .message-row.user .message-bubble { background-color: #0A84FF; }
.ios-frame.dark .date-divider { background-color: rgba(255,255,255,0.15); color: #AEAEB2; }

/* Scrollbar Dark */
.ios-frame.dark .chat-container::-webkit-scrollbar-thumb { background-color: rgba(255, 255, 255, 0.25); }
.ios-frame.dark .chat-container::-webkit-scrollbar-thumb:hover { background-color: rgba(255, 255, 255, 0.4); }

/* Input */
.ios-frame.dark .input-area { background-color: #1C1C1E; border-top-color: #38383A; }
.ios-frame.dark .input-container { background-color: #2C2C2E; border-color: #38383A; }
.ios-frame.dark input { color: #FFF; }
.ios-frame.dark input::placeholder { color: #8E8E93; }

/* Links & Markdown */
:deep(.product-link) { color: #007AFF; font-weight: 700; text-decoration: underline; cursor: pointer; }
.ios-frame.dark :deep(.product-link) { color: #64D2FF; }
:deep(.markdown-body p) { margin: 0 0 4px 0; }
:deep(.markdown-body ul) { margin: 4px 0 4px 20px; padding: 0; }
</style>