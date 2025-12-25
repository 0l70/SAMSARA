<template>
  <div class="home-container">
    
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="main-title">
          <span class="highlight">{{ typeValue }}</span>
          <span class="cursor" :class="{ typing: typeStatus }">&nbsp;</span>
          <br>
          <span class="static-text">내 자산의 모든 것</span>
        </h1>
        <p class="sub-title">
          복잡한 금융 생활, <strong>FinBot</strong>으로 심플하게.<br>
        </p>
      </div>
    </section>

    <section class="dashboard-grid">
      
  <div class="card profile-card">
    <div v-if="store.token" class="profile-content logged-in">
      
      <div v-if="mbtiInfo" class="character-area">
        <div class="avatar-circle" :style="{ backgroundColor: mbtiInfo.bg }">
          <span class="char-icon" role="img">{{ mbtiInfo.icon }}</span>
        </div>
        <div class="user-info">
          <div class="mbti-badge" :style="{ color: mbtiInfo.color, borderColor: mbtiInfo.color }">
            {{ mbtiInfo.label }}
          </div>
          <h3 class="welcome-text">
            <span class="highlight-name">{{ store.nickname || '회원' }}</span>님
          </h3>
          <p class="sub-text">오늘도 자산이 쑥쑥 자라고 있어요! 🌱</p>
        </div>
      </div>

      <div v-else class="character-area no-mbti">
        <div class="avatar-circle default">
          <span class="char-icon">❔</span>
        </div>
        <div class="user-info">
          <h3 class="welcome-text">
            <span class="highlight-name">{{ store.nickname || '회원' }}</span>님
          </h3>
          <p class="sub-text">나만의 금융 캐릭터를 찾아보세요!</p>
          <button class="btn-test-action" @click="goTest">
            내 성향 알아보기 📝
          </button>
        </div>
      </div>


    <div class="profile-actions">
      <button class="btn-mypage" @click="router.push({ name: 'mypage' })">마이페이지</button>
      <button class="btn-logout" @click="store.logOut()">로그아웃</button>
    </div>
  </div>

  <div v-else class="profile-content login-form-container">
    <div class="login-header">
      <h3>로그인</h3>
      <p>서비스 이용을 위해 로그인해주세요</p>
    </div>
    <form @submit.prevent="handleLogin" class="login-form">
      <input v-model="loginData.username" type="text" placeholder="아이디" required class="login-input" />
      <input v-model="loginData.password" type="password" placeholder="비밀번호" required class="login-input" />
      <button type="submit" class="btn-login-action">로그인 하기</button>
    </form>
    <div class="login-footer">
      <span @click="router.push({ name: 'signup' })" class="link-text">회원가입 하러가기</span>
    </div>
  </div>
</div>

      <div class="card clock-card">
        <div class="clock-header">
          <span class="date-text">{{ currentDate }}</span>
          <span class="market-badge" :class="{ open: isMarketOpen }">
            {{ isMarketOpen ? '● 장 운영중' : '○ 장 마감' }}
          </span>
        </div>
        <div class="clock-body">
          <div class="time-big">{{ currentTime }}</div>
        </div>
        <div class="weather-footer">
          <div class="weather-info">
            <component :is="weatherIconComponent" class="weather-icon-svg" />
            <span class="weather-temp">{{ weatherTemp }}°</span>
            <span class="weather-desc">{{ weatherDesc }}</span>
          </div>
          <span class="location-text">Seoul</span>
        </div>
      </div>

      <div class="card menu-card">
        <h3>바로가기</h3>
        <div class="menu-list">
          <div class="menu-item" @click="router.push({ name: 'BankView' })">
            <div class="menu-icon blue"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21v-7"/><path d="M19 21v-7"/><path d="M2 10h20"/><path d="M12 3L2 10v3h20v-3z"/></svg></div>
            <span>은행 찾기</span>
          </div>
          <div class="menu-item" @click="router.push({ name: 'products' })">
            <div class="menu-icon orange"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg></div>
            <span>금리 비교</span>
          </div>
          <div class="menu-item" @click="router.push({ name: 'chatbot' })">
            <div class="menu-icon green"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2 2 2 0 0 1-2-2V4a2 2 0 0 1 2-2Z"/><path d="M4 9v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9"/><path d="M10 17h4v5h-4z"/></svg></div>
            <span>AI 비서</span>
          </div>
        </div>
      </div>

      <div class="card subscription-card" @click="router.push({ name: 'subscription-list' })">
        <div class="card-header">
          <div class="header-title-box">
            <div class="header-icon-wrapper">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>
            </div>
            <h3>내 구독 상품</h3>
          </div>
          <span v-if="store.token && myRealProducts.length > 0" class="count-badge">{{ myRealProducts.length }}</span>
        </div>

        <div class="card-body">
          <div v-if="!store.token" class="blur-overlay-container">
            <div class="blur-content">
              <div class="lock-icon-box">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
              </div>
              <p>로그인하고 내 자산을<br>한눈에 관리하세요</p>
            </div>
            <ul class="sub-list dummy">
              <li class="sub-item"><div class="dummy-bar short"></div><div class="dummy-bar long"></div></li>
              <li class="sub-item"><div class="dummy-bar short"></div><div class="dummy-bar long"></div></li>
            </ul>
          </div>

          <div v-else-if="myRealProducts.length > 0" class="product-scroll-area">
            <div v-for="product in myRealProducts" :key="product.fin_prdt_cd" class="preview-item">
              <div class="item-info">
                <span class="preview-bank">{{ product.kor_co_nm }}</span>
                <span class="preview-name">{{ product.fin_prdt_nm }}</span>
              </div>
              <div v-if="product.options && product.options[0]" class="sub-rate">
                {{ product.options[0].intr_rate2 }}%
              </div>
              <span v-else class="status-dot"></span>
            </div>
          </div>

          <div v-else class="empty-state-mini">
            <div class="empty-icon-box">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
            </div>
            <p>아직 가입한 상품이 없어요</p>
            <button @click.stop="router.push({ name: 'products' })" class="btn-text">금리 높은 상품 찾기 →</button>
          </div>
        </div>
      </div>

      <div class="card news-card">
        <div class="card-header">
          <div class="header-title-box">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="header-icon"><path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"></path><path d="M18 14h-8"></path><path d="M15 18h-5"></path><path d="M10 6h8v4h-8V6Z"></path></svg>
            <h3>주요 금융 뉴스</h3>
          </div>
          <span class="live-badge">LIVE</span>
        </div>
        <div v-if="loadingNews" class="loading-state">뉴스를 불러오는 중...</div>
        <ul v-else class="news-list">
          <li v-for="(news, index) in newsList" :key="index" class="news-item">
            <a :href="news.link" target="_blank" class="news-link">
              <span class="news-text" v-html="news.title"></span>
              <span class="news-ago">{{ timeAgo(news.pubDate) }}</span>
            </a>
          </li>
        </ul>
      </div>

      <div class="card tip-card full-width">
        <div class="tip-content">
          <div class="tip-icon-box">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#d97706" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-1 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"></path><path d="M9 18h6"></path><path d="M10 22h4"></path></svg>
          </div>
          <span class="tip-text">{{ todayTip }}</span>
        </div>
      </div>

    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, h, shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFinanceStore } from '@/stores/finance'
import axios from 'axios'

const router = useRouter()
const store = useAuthStore()
const financeStore = useFinanceStore()

const mbtiInfo = computed(() => {
  const mbti = store.mbti // store에 mbti 정보가 있다고 가정 (없으면 user API 호출 필요)
  
  const map = {
    safe: { icon: '🐜', label: '성실한 개미', color: '#84cc16', bg: '#ecfccb' },      // 라임색
    neutral: { icon: '🐹', label: '신중한 햄스터', color: '#f59e0b', bg: '#fef3c7' }, // 호박색
    active: { icon: '🦊', label: '똑똑한 여우', color: '#f97316', bg: '#ffedd5' },    // 주황색
    aggressive: { icon: '🦁', label: '용감한 사자', color: '#ef4444', bg: '#fee2e2' } // 빨간색
  }
  
  return map[mbti] || null // 매칭되는 게 없으면 null (테스트 안 한 상태)
})

// 2. 테스트 페이지 이동 함수
const goTest = () => router.push({ name: 'test' })


// ----------------------------------------------------
// [0] 로그인 로직 (Inline Login)
// ----------------------------------------------------
const loginData = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginData.username || !loginData.password) {
    alert("아이디와 비밀번호를 모두 입력해주세요.")
    return
  }
  try {
    await store.logIn({
      username: loginData.username,
      password: loginData.password
    })
    financeStore.getProducts()
  } catch (error) {
    console.error(error)
    alert("로그인 정보가 올바르지 않습니다.")
  }
}

// ----------------------------------------------------
// [1] 날씨 아이콘 & 로직 (Open-Meteo)
// ----------------------------------------------------
const SunIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
  h('circle', { cx: 12, cy: 12, r: 4 }),
  h('path', { d: 'M12 2v2' }), h('path', { d: 'M12 20v2' }),
  h('path', { d: 'M4.93 4.93l1.41 1.41' }), h('path', { d: 'M17.66 17.66l1.41 1.41' }),
  h('path', { d: 'M2 12h2' }), h('path', { d: 'M20 12h2' }),
  h('path', { d: 'M6.34 17.66l-1.41 1.41' }), h('path', { d: 'M19.07 4.93l-1.41 1.41' })
])
const MoonIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
  h('path', { d: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' })
])
const CloudIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
  h('path', { d: 'M17.5 19c0-3.037-2.463-5.5-5.5-5.5S6.5 15.963 6.5 19' }),
  h('path', { d: 'M17.5 19h-11' }),
  h('path', { d: 'M12 13.5a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9' })
])
const RainIcon = () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
  h('path', { d: 'M16 13v8' }), h('path', { d: 'M8 13v8' }), h('path', { d: 'M12 15v8' }),
  h('path', { d: 'M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25' })
])

const currentTime = ref('')
const currentDate = ref('')
const isMarketOpen = ref(false)
const weatherTemp = ref('--')
const weatherDesc = ref('Loading')
const weatherIconComponent = shallowRef(SunIcon)

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('ko-KR', { hour12: false, hour: '2-digit', minute: '2-digit' })
  currentDate.value = now.toLocaleDateString('ko-KR', { month: 'long', day: 'numeric', weekday: 'short' })
  const day = now.getDay(); const hour = now.getHours()
  isMarketOpen.value = (day >= 1 && day <= 5 && hour >= 9 && hour < 16)
}

const fetchWeather = async () => {
  try {
    const url = 'https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&current_weather=true&timezone=auto'
    const res = await axios.get(url)
    const data = res.data.current_weather
    
    weatherTemp.value = Math.round(data.temperature)
    const code = data.weathercode
    
    if (code === 0) { weatherDesc.value = '맑음'; weatherIconComponent.value = SunIcon }
    else if (code >= 1 && code <= 3) { weatherDesc.value = '구름'; weatherIconComponent.value = CloudIcon }
    else if (code >= 51) { weatherDesc.value = '비/눈'; weatherIconComponent.value = RainIcon }
    else { weatherDesc.value = '흐림'; weatherIconComponent.value = CloudIcon }

    const h = new Date().getHours()
    if ((h > 19 || h < 6) && code === 0) weatherIconComponent.value = MoonIcon

  } catch (e) {
    weatherTemp.value = 20; weatherDesc.value = '-'
  }
}

// ----------------------------------------------------
// [2] 뉴스 (Google News RSS Proxy)
// ----------------------------------------------------
const newsList = ref([])
const loadingNews = ref(true)

const fetchNews = async () => {
  try {
    const rssUrl = 'https://news.google.com/rss/search?q=금융+경제&hl=ko&gl=KR&ceid=KR:ko'
    const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`
    const res = await axios.get(apiUrl)
    if (res.data.items) {
      newsList.value = res.data.items.slice(0, 5)
    }
  } catch (e) {
    console.error(e)
  } finally {
    loadingNews.value = false
  }
}
const timeAgo = (dateStr) => {
  const diff = new Date() - new Date(dateStr)
  const m = Math.floor(diff / 60000)
  if (m < 60) return `${m}분 전`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}시간 전`
  return `${Math.floor(h/24)}일 전`
}

// ----------------------------------------------------
// [3] 내 구독 상품
// ----------------------------------------------------
const myRealProducts = computed(() => {
  return financeStore.joinedProducts || []
})

// ----------------------------------------------------
// [4] 기타 (Typing Effect)
// ----------------------------------------------------
const typeValue = ref(''); const typeStatus = ref(false)
const typeArray = ['적금 들걸...', '투자 할걸...', '공부 할걸...', '삼사라 할걸...']
const todayTip = "신용카드는 한도의 50% 이하로 사용할 때 신용점수에 가장 좋습니다."
let timer = null; let typeIdx = 0; let charIdx = 0

const typeText = () => {
  if (charIdx < typeArray[typeIdx].length) {
    typeStatus.value = true
    typeValue.value += typeArray[typeIdx].charAt(charIdx++)
    setTimeout(typeText, 100)
  } else {
    typeStatus.value = false
    setTimeout(eraseText, 1500)
  }
}
const eraseText = () => {
  if (charIdx > 0) {
    typeStatus.value = true
    typeValue.value = typeArray[typeIdx].substring(0, charIdx - 1)
    charIdx--
    setTimeout(eraseText, 50)
  } else {
    typeStatus.value = false
    typeIdx = (typeIdx + 1) % typeArray.length
    setTimeout(typeText, 1000)
  }
}

onMounted(() => {
  updateTime(); fetchWeather(); fetchNews()
  timer = setInterval(updateTime, 1000)
  setTimeout(typeText, 1000)
  
  if (store.token) {
    financeStore.getProducts() 
  }
})
onUnmounted(() => { if(timer) clearInterval(timer) })
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

:root {
  --bg-card: #ffffff;
  --text-primary: #1f2937;
  --text-secondary: #4b5563;
  --text-muted: #9ca3af;
  --bg-hover: #f9fafb;
  --border-color: #f3f4f6;
  --primary: #3b82f6;
}

.home-container {
  max-width: 1000px; margin: 0 auto; padding: 40px 20px 80px;
  font-family: 'Pretendard', sans-serif; color: var(--text-primary);
}

/* Hero Section */
.hero-section { text-align: center; margin-bottom: 50px; }
.main-title { font-size: 2.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 10px; }
.highlight { color: var(--primary); }
.cursor { border-right: 3px solid var(--text-primary); animation: blink 1s infinite; }
.cursor.typing { animation: none; }
.sub-title { font-size: 1.1rem; color: var(--text-secondary); opacity: 0.8; }

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Card Common */
.card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 24px;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  transition: transform 0.2s, box-shadow 0.2s;
  overflow: hidden;
  display: flex; flex-direction: column;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.card-header h3 { font-size: 1.1rem; font-weight: 700; margin: 0; }
.header-title-box { display: flex; align-items: center; gap: 8px; }
.header-icon { color: var(--text-secondary); }

/* 1. Profile Card */
.profile-card { grid-column: span 1; justify-content: center; align-items: center; text-align: center; }
.profile-content { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 12px; }

/* Logged In Style */
.avatar-circle { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: #eff6ff; color: var(--primary); margin-bottom: 10px; }
.welcome-text { margin: 0; font-size: 1.4rem; font-weight: 800; line-height: 1.4; color: var(--text-primary); }
.highlight-name { color: var(--primary); }
.sub-text { margin: 4px 0 0; font-size: 0.95rem; color: var(--text-muted); }
/* 1. 버튼들을 감싸는 영역: 중앙 정렬 및 간격 */
.profile-actions {
  display: flex;
  gap: 10px;               /* 버튼 사이 간격 */
  justify-content: center; /* 가로 중앙 정렬 */
  width: 100%;
  padding: 0 20px;         /* 양옆 여백 */
  margin-top: 24px;
}

.btn-mypage, .btn-logout {
  /* 크기 설정 */
  flex: 1;                 /* 반반씩 너비 차지 */
  height: 52px;            /* 이미지의 도톰한 높이감 */
  border-radius: 14px;     /* 부드러운 곡선형 모서리 */
  
  /* 폰트 설정 */
  font-size: 16px;         /* 가독성 좋은 크기 */
  font-weight: 700;        /* 굵은 폰트 적용 (이미지 핵심) */
  letter-spacing: -0.5px;  /* 자간을 좁혀 세련된 느낌 */
  
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* 마이페이지: 선명한 블루 버튼 */
.btn-mypage {
  background-color: #3182f6;
  color: #ffffff;
  border: none;
}

/* 로그아웃: 흰색 배경에 아주 연한 테두리 */
.btn-logout {
  background-color: #ffffff;
  color: #8b95a1;           /* 이미지 속 연한 회색 글자 */
  border: 1px solid #f2f4f6; /* 눈에 띄지 않을 정도의 연한 테두리 */
}

/* 클릭 효과 */
.btn-mypage:active {
  background-color: #1b64da;
  transform: scale(0.98);    /* 누를 때 살짝 들어가는 효과 */
}

.btn-logout:active {
  background-color: #f9fafb;
  transform: scale(0.98);
}
/* Login Form */
.login-form-container { width: 100%; padding: 0 4px; }
.login-header h3 { font-size: 1.3rem; font-weight: 700; margin-bottom: 4px; }
.login-header p { font-size: 0.9rem; color: var(--text-muted); margin: 0 0 20px 0; }
.login-form { width: 100%; display: flex; flex-direction: column; gap: 12px; position: relative; }
.login-input { width: 100%; padding: 12px; border: 1px solid #e5e7eb; border-radius: 12px; font-size: 0.95rem; outline: none; transition: all 0.2s; box-sizing: border-box; background: #f9fafb; }
.login-input:focus { border-color: var(--primary); background: #fff; }

.btn-login-action { 
  width: 100%; 
  background: #3b82f6; 
  color: white; 
  padding: 12px; 
  border-radius: 12px; 
  font-weight: 700; 
  border: none; 
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.2s ease;
}

.btn-login-action:hover {
  background: #2563eb;
}


/* 2. 로그인 후: 환영 메시지 스타일 */
.welcome-text {
  font-size: 1.4rem;
  font-weight: 800;
  line-height: 1.4;
  margin: 10px 0;
  color: #1f2937;
}

.highlight-name {
  color: #3b82f6; /* 닉네임 강조색 */
}

.avatar-circle {
  width: 60px;
  height: 60px;
  background: #eff6ff;
  color: #3b82f6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

/* 기타 스타일 보정 */
.login-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  margin-bottom: 8px;
  box-sizing: border-box;
}

.sub-text {
  font-size: 0.9rem;
  color: #6b7280;
}

.btn-logout {
  font-size: 0.8rem;
  color: #9ca3af;
  background: none;
  border: 1px solid #f3f4f6;
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.btn-login-action:hover { background: #2563eb; }
.login-footer { margin-top: 16px; font-size: 0.85rem; color: var(--text-muted); }
.link-text { color: var(--primary); font-weight: 600; cursor: pointer; margin-left: 6px; }
.link-text:hover { text-decoration: underline; }

/* 2. Clock & Weather */
.clock-card { 
  background: linear-gradient(135deg, #2563eb 0%, #60a5fa 100%); 
  color: white; border: none; justify-content: space-between; position: relative;
}
.clock-header { display: flex; justify-content: space-between; opacity: 0.9; font-size: 0.9rem; font-weight: 500; }
.clock-body { text-align: center; margin: 24px 0; }
.time-big { font-size: 3.2rem; font-weight: 800; letter-spacing: -2px; line-height: 1; }
.weather-footer { display: flex; justify-content: space-between; align-items: flex-end; }
.weather-info { display: flex; align-items: center; gap: 8px; }
.weather-icon-svg { width: 32px; height: 32px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); }
.weather-temp { font-size: 1.8rem; font-weight: 700; }
.weather-desc { font-size: 1rem; opacity: 0.9; margin-left: 4px; }
.market-badge.open { color: #6ee7b7; font-weight: 700; }

/* 3. Menu Card */
.menu-list { display: flex; flex-direction: column; gap: 10px; height: 100%; justify-content: center; }
.menu-item { display: flex; align-items: center; gap: 14px; padding: 12px; border-radius: 16px; cursor: pointer; transition: background 0.2s; }
.menu-item:hover { background: var(--bg-hover); }
.menu-icon { width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.menu-icon svg { width: 24px; height: 24px; }
.menu-icon.blue { background: #eff6ff; color: #2563eb; }
.menu-icon.orange { background: #fff7ed; color: #ea580c; }
.menu-icon.green { background: #f0fdf4; color: #16a34a; }
.menu-item span { font-weight: 600; font-size: 1rem; }

/* 4. Subscription Card */
.subscription-card { grid-column: span 2; min-height: 240px; }
/* 카드 기본 설정 */
/* 1. 부모 카드: 하단 패딩을 거의 없애서 리스트가 아래까지 내려오게 함 */
.subscription-card {
  background: #ffffff;
  border-radius: 24px;
  padding: 24px 24px 0px 24px; /* 하단(bottom) 패ding을 10px로 최소화 */
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f2f4f6;
  display: flex;
  flex-direction: column;
  gap: 16px;            /* 헤더와 리스트 사이 간격을 좁혀서 공간 확보 */
  overflow: hidden; 
  min-height: 250px;    /* 카드 자체의 최소 높이를 키워서 시원하게 만듦 */
}

/* 2. 스크롤 영역: max-height를 대폭 늘려 세로로 길게 확장 */
.product-scroll-area {
  /* 150px -> 380px로 확장 (더 많은 아이템이 한 번에 보임) */
  max-height: 380px;    
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-right: 6px;   /* 스크롤바와 아이템 사이 간격 */
  padding-bottom: 15px; /* 리스트 맨 끝 아이템이 잘려 보이지 않게 여유분 */
}

/* 3. 리스트 아이템: 높이감을 주어 가독성 향상 */
.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;   /* 상하 패딩을 늘려 아이템 하나하나를 큼직하게 */
  background-color: #f9fafb;
  border-radius: 16px;
  transition: all 0.2s;
}

.preview-item:hover {
  background-color: #f2f4f6;
  transform: scale(1.01); /* 마우스 올렸을 때 살짝 커지는 효과 */
}

/* 4. 스크롤바 디자인: 가늘고 깔끔하게 (답답함 해소) */
.product-scroll-area::-webkit-scrollbar {
  width: 4px;
}

.product-scroll-area::-webkit-scrollbar-thumb {
  background-color: #e5e8eb;
  border-radius: 10px;
}

/* 스크롤바가 너무 굵으면 가려지는 느낌이 드니 얇게 조정 */
.product-scroll-area::-webkit-scrollbar {
  width: 4px;
}

.subscription-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
  background-color: #fafafa;
}

/* 헤더 섹션 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title-box {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon-wrapper {
  width: 36px;
  height: 36px;
  background: #f2f4f6;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4e5968;
}

.header-title-box h3 {
  font-size: 18px;
  font-weight: 700;
  color: #191f28;
  margin: 0;
}

/* 숫자 뱃지 */
.count-badge {
  background: #f2f4f6;
  color: #3182f6;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
}

/* 바디 섹션 - 상태 메시지 */
.state-msg {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #8b95a1;
  font-size: 15px;
  font-weight: 500;
}

.action-link {
  color: #3182f6;
  font-size: 14px;
  font-weight: 600;
}

/* 상품 미리보기 리스트 */
.product-preview-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.preview-bank {
  font-size: 13px;
  font-weight: 600;
  color: #4e5968;
  background: #f9fafb;
  padding: 2px 8px;
  border-radius: 6px;
  white-space: nowrap;
}

.preview-name {
  font-size: 15px;
  color: #333d4b;
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-text {
  font-size: 13px;
  color: #adb5bd;
  margin-top: 4px;
}
.count-badge { background: #eff6ff; color: var(--primary); padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight: 700; }
.sub-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.sub-item { display: flex; align-items: center; gap: 16px; padding: 12px 16px; border: 1px solid var(--border-color); border-radius: 16px; cursor: pointer; transition: all 0.2s; }
.sub-item:hover { border-color: var(--primary); background: #eff6ff; }
.bank-logo { width: 42px; height: 42px; border-radius: 50%; background: #f3f4f6; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #6b7280; font-size: 0.9rem; flex-shrink: 0; }
.sub-info { flex: 1; display: flex; flex-direction: column; }
.sub-bank { font-size: 0.8rem; color: var(--text-muted); }
.sub-name { font-weight: 700; font-size: 1rem; }
.sub-rate { color: #ef4444; font-weight: 700; font-size: 1.1rem; }
.empty-state { padding: 40px 0; text-align: center; color: var(--text-muted); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }
.empty-icon-box { margin-bottom: 8px; opacity: 0.5; }
.btn-text { background: none; border: none; color: var(--primary); font-weight: 600; cursor: pointer; margin-top: 5px; font-size: 0.95rem; }

/* Blur Overlay */
.blur-overlay-container { position: relative; height: 100%; overflow: hidden; border-radius: 12px; }
.blur-content { 
  position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10;
  background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(5px);
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
}
.lock-icon-box { width: 50px; height: 50px; background: rgba(0,0,0,0.05); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; color: var(--text-secondary); }
.blur-content p { font-weight: 700; color: var(--text-primary); margin: 0; font-size: 1.05rem; line-height: 1.5; }
.dummy .sub-item { opacity: 0.3; border-color: transparent; background: #f9fafb; cursor: default; pointer-events: none; }
.dummy-bar { background: #e5e7eb; border-radius: 4px; height: 14px; }
.dummy-bar.short { width: 42px; height: 42px; border-radius: 50%; }
.dummy-bar.long { flex: 1; height: 20px; }

/* 5. News Card */
.news-card { grid-column: span 1; display: flex; flex-direction: column; }
.live-badge { background: #ef4444; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; animation: pulse 2s infinite; }
.loading-state { text-align: center; color: var(--text-muted); margin-top: 40px; }
.news-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 14px; flex: 1; }
.news-link { text-decoration: none; display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
.news-text { color: var(--text-primary); font-size: 0.95rem; line-height: 1.4; font-weight: 500; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.news-link:hover .news-text { color: var(--primary); text-decoration: underline; }
.news-ago { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; margin-top: 2px; }

/* 6. Tip Card */
.full-width { grid-column: span 3; background: #fffbeb; border: 1px solid #fcd34d; padding: 16px 24px; min-height: auto; flex-direction: row; align-items: center; }
.tip-content { display: flex; align-items: center; gap: 12px; color: #92400e; font-weight: 600; font-size: 1rem; }
.tip-icon-box svg { width: 24px; height: 24px; }


/* 1. 스크롤 컨테이너 설정 */
.product-scroll-area {
  max-height: 220px;       /* 카드가 너무 커지지 않도록 높이 제한 */
  overflow-y: auto;        /* 세로 스크롤 활성화 */
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-right: 4px;      /* 스크롤바와 아이템 사이 여백 */
}

/* 2. 개별 아이템 디자인 */
.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background-color: #f9fafb;
  border-radius: 12px;
  transition: background-color 0.2s;
}

.preview-item:hover {
  background-color: #f2f4f6; /* 마우스 올리면 살짝 더 어둡게 */
}

.item-info {
  display: flex;
  flex-direction: column;  /* 은행과 상품명을 세로로 배치하여 가독성 업 */
  gap: 2px;
  overflow: hidden;
}

.preview-bank {
  font-size: 11px;
  font-weight: 700;
  color: #3182f6;          /* 은행명 강조 */
}

.preview-name {
  font-size: 14px;
  font-weight: 500;
  color: #333d4b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis; /* 상품명이 길면 말줄임표 */
}

/* 3. 활성화 표시 점 */
.status-dot {
  width: 6px;
  height: 6px;
  background-color: #3182f6;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 4. 깔끔한 커스텀 스크롤바 */
.product-scroll-area::-webkit-scrollbar {
  width: 4px;              /* 스크롤바 너비 */
}

.product-scroll-area::-webkit-scrollbar-thumb {
  background-color: #e5e8eb; /* 스크롤바 색상 */
  border-radius: 4px;
}

.product-scroll-area::-webkit-scrollbar-track {
  background-color: transparent;
}
/* Animation */
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.6; } 100% { opacity: 1; } }

/* Responsive */
@media (max-width: 900px) {
  .dashboard-grid { grid-template-columns: 1fr 1fr; }
  .profile-card { grid-column: span 1; }
  .clock-card { grid-column: span 1; }
  .menu-card { grid-column: span 2; flex-direction: row; align-items: center; }
  .menu-list { flex-direction: row; width: 100%; justify-content: space-around; }
  .subscription-card { grid-column: span 2; }
  .news-card { grid-column: span 2; }
  .full-width { grid-column: span 2; }
}

@media (max-width: 600px) {
  .dashboard-grid { display: flex; flex-direction: column; }
}

.character-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  width: 100%;
}

/* 아바타(캐릭터) 원형 스타일 */
.avatar-circle {
  width: 80px;        /* 크기 키움 */
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
  position: relative;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.avatar-circle:hover {
  transform: scale(1.1) rotate(5deg); /* 마우스 올리면 커지면서 살짝 회전 */
}

.char-icon {
  font-size: 42px;    /* 이모지 크기 */
  line-height: 1;
  animation: float 3s ease-in-out infinite; /* 둥실둥실 효과 */
}

/* 테스트 전 기본 상태 */
.avatar-circle.default {
  background-color: #f3f4f6;
  border: 2px dashed #d1d5db;
}

/* MBTI 뱃지 (예: 성실한 개미) */
.mbti-badge {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 12px;
  border: 1px solid; /* 색상은 인라인 스타일로 들어감 */
  background: white;
  margin-bottom: 6px;
}

/* 테스트 하러 가기 버튼 (강조) */
.btn-test-action {
  margin-top: 8px;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
  transition: all 0.2s;
  animation: pulse-btn 2s infinite;
}

.btn-test-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(59, 130, 246, 0.4);
}

/* 애니메이션 키프레임 */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes pulse-btn {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}

/* 텍스트 정리 */
.welcome-text { margin: 0; font-size: 1.5rem; }
.sub-text { margin-top: 5px; color: #6b7280; font-size: 0.95rem; }

</style>