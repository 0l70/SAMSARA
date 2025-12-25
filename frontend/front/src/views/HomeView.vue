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
        <div class="card-header">
          <div class="header-title-box">
            <div class="header-icon-wrapper" style="background-color: rgba(74, 134, 232, 0.1); color: #4a86e8;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
              </svg>
            </div>
            <h3 class="h3-title" style="margin: 0;">바로가기</h3>
          </div>
        </div>
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

const lastUpdatedNews = ref('');

const fetchNews = async () => {
  try {
    loadingNews.value = true;
    const rssUrl = 'https://news.google.com/rss/search?q=금융+경제&hl=ko&gl=KR&ceid=KR:ko';
    const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`;
    const res = await axios.get(apiUrl);
    
    if (res.data.items) {
      newsList.value = res.data.items.slice(0, 5);
      // 마지막 업데이트 시간 기록
      const now = new Date();
      lastUpdatedNews.value = `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`;
    }
  } catch (e) {
    console.error(e);
  } finally {
    loadingNews.value = false;
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
const tips = [
  "신용카드는 한도의 50% 이하로 사용할 때 신용점수 관리에 가장 유리합니다.",
  "월급의 10%는 무조건 비상금 통장에 먼저 이체하는 습관을 가져보세요.",
  "신용점수를 올리고 싶다면 체크카드와 신용카드를 7:3 비율로 섞어 써보세요.",
  "복리의 마법을 누리려면 하루라도 빨리 저축과 투자를 시작하는 것이 좋습니다.",
  "통신비나 공공요금 납부 내역을 신용평가사에 제출하면 신용점수가 올라갑니다.",
  "연말정산 세액공제를 위해 IRP나 연금저축 계좌를 활용하는 것을 잊지 마세요.",
  "고정 지출 중 사용하지 않는 구독 서비스만 정리해도 매달 커피 몇 잔 값을 아낍니다.",
  "대출을 갚을 때는 금리가 가장 높은 대출부터 먼저 상환하는 것이 경제적입니다.",
  "CMA 통장은 하루만 맡겨도 이자가 붙어 비상금 통장으로 활용하기 좋습니다.",
  "주거래 은행만 고집하기보다 금리 비교 사이트를 통해 가장 유리한 상품을 찾으세요."
];
const todayTip = tips[Math.floor(Math.random() * tips.length)];
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

// 1. 스크립트 상단에 타이머 변수 선언 (onMounted 밖에서 정의)
let newsTimer = null; 

// 2. onMounted 수정
onMounted(() => {
  // [초기 실행] 페이지 접속 시 즉시 데이터 호출
  updateTime();
  fetchWeather();
  fetchNews();
  
  // [시계] 1초마다 시간 업데이트
  timer = setInterval(updateTime, 1000);
  
  // [뉴스] 1시간(3,600,000ms)마다 뉴스 새로고침
  newsTimer = setInterval(fetchNews, 3600000); 

  // [기타 효과] 타이핑 효과 시작
  setTimeout(typeText, 1000);
  
  // [유저 데이터] 로그인 상태라면 상품 정보 로드
  if (store.token) {
    financeStore.getProducts();
  }
});

// 3. onUnmounted 수정 (모든 타이머 해제)
onUnmounted(() => {
  if (timer) clearInterval(timer);
  if (newsTimer) clearInterval(newsTimer); // 뉴스 타이머도 반드시 해제!
});
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

/* ===============================
   🌙 Dark Mode Variables
   =============================== */
[data-theme="dark"] {
  --bg-card: #1e293b;        /* 카드 배경 */
  --text-primary: #e5e7eb;   /* 메인 텍스트 */
  --text-secondary: #cbd5f5; /* 서브 텍스트 */
  --text-muted: #94a3b8;
  --bg-hover: #334155;
  --border-color: #334155;
  --primary: #60a5fa;
}

.h3-title {
  margin-top: 0%;
}
.home-container {
  max-width: 1000px; margin: 0 auto; padding: 13px 20px 80px;
  font-family: 'Pretendard', sans-serif; color: var(--text-primary);
}

/* Hero Section */
.hero-section { text-align: center; margin-bottom: 50px; }
.main-title { font-size: 2.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 10px; }
.highlight { color: var(--primary); }
.cursor {
  display: inline-block;
  vertical-align: middle; /* 글자 높이 중앙에 맞춤 */
  width: 0;               /* 너비를 0으로 해서 배경색 블럭 방지 */
  height: 1.2em;          /* 커서 길이를 글자보다 살짝 길게 */
  border-right: 2px solid #3182f6; /* 배경 대신 테두리(선)만 사용 */
  margin-left: 2px;       /* 글자와의 간격 */
  animation: blink 1s step-end infinite; /* 깜빡임을 더 깔끔하게(step-end) */
}
.cursor.typing { animation: none; }
.sub-title { font-size: 1.1rem; color: var(--text-secondary); opacity: 0.8; }
/* 다크모드: 선 색상만 살짝 밝게 */
[data-theme="dark"] .cursor {
  border-right-color: #4a94ff;
}
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
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between; /* 제목은 왼쪽, 뱃지는 오른쪽 */
  padding-bottom: 12px;
}
.card-header h3 { font-size: 1.1rem; font-weight: 700; margin: 0; }
.header-title-box { display: flex; align-items: center; gap: 8px; }
.header-icon { color: var(--text-secondary); }

/* 1. 다크모드일 때 호버 효과를 배경색과 똑같이 맞춤 (파란색 제거) */
[data-theme="dark"] .card:hover, 
[data-theme="dark"] .feature-card:hover {
  background-color: var(--bg-card) !important; /* 파란색 대신 원래 카드 배경색 유지 */
  border-color: var(--border-color) !important; /* 테두리 파란색 방지 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important; /* 파란 그림자 대신 어두운 그림자 */
  transform: translateY(-5px); /* 움직임은 유지하고 싶다면 남겨두고, 싫으면 none으로 변경 */
}

/* 2. 만약 텍스트도 파란색으로 변한다면 */
[data-theme="dark"] .card:hover h3,
[data-theme="dark"] .card:hover p {
  color: var(--text-primary) !important;
}

[data-theme="dark"] .menu-item:hover,
[data-theme="dark"] .preview-item:hover {
  background-color: var(--bg-hover);
}

[data-theme="dark"] .sub-item {
  background-color: #1f2937;
}

[data-theme="dark"] .news-text {
  color: var(--text-primary);
}

[data-theme="dark"] .news-link:hover .news-text {
  color: var(--primary);
}

[data-theme="dark"] .clock-card {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

[data-theme="dark"] .tip-card {
  background: #1e293b;
  border-color: #334155;
}

[data-theme="dark"] .tip-text {
  color: #facc15;
}

[data-theme="dark"] .blur-content {
  background: rgba(15, 23, 42, 0.7);
  color: var(--text-primary);
}

/* 다크모드에서 .blur-content 호버 시 파란색 반응 제거 */
[data-theme="dark"] .blur-content:hover {
  /* 1. 배경색을 파란색 대신 투명하거나 어두운 배경으로 고정 */
  background-color: rgba(255, 255, 255, 0.05) !important; 
  
  /* 2. 테두리에 파란색이 있다면 기본 테두리 색상으로 유지 */
  border-color: var(--border-color) !important;
  
  /* 3. 파란색 글로우(그림자) 효과 제거 */
  box-shadow: none !important;
  
  /* 4. 내부 글자색이 파란색으로 변하는 경우 방지 */
  color: var(--text-primary) !important;
}

/* 만약 가상 요소(::before, ::after)로 파란빛을 내고 있다면 이것도 초기화 */
[data-theme="dark"] .blur-content:hover::before,
[data-theme="dark"] .blur-content:hover::after {
  background: none !important;
  display: none;
}

/* 🌙 Dark Mode - Welcome Text */
[data-theme="dark"] .welcome-text {
  color: var(--text-primary);
}

[data-theme="dark"] .highlight-name {
  color: var(--primary);
}

/* 🌙 Dark Mode - News Card Title */
[data-theme="dark"] .news-card .header-title-box h3 {
  color: var(--text-primary);
}

[data-theme="dark"] .news-card .header-icon {
  color: var(--text-secondary);
}


/* 🌙 Dark Mode - Subscription Card */
[data-theme="dark"] .subscription-card {
  background: var(--bg-card);
  border-color: var(--border-color);
}

/* 내부 리스트 */
[data-theme="dark"] .subscription-card .preview-item {
  background-color: rgba(255, 255, 255, 0.03);
  color: var(--text-secondary);
  font-weight: 400;
}


[data-theme="dark"] .subscription-card .preview-item:hover {
  background-color: rgba(255, 255, 255, 0.06);
}

/* 🌙 Dark Mode - Subscription Count Badge */
[data-theme="dark"] .subscription-card .count-badge {
  color: #020617;                 /* 거의 검정 */
  background-color: #e5e7eb;      /* 연한 회색 */
  border: none;
  box-shadow: none;

  font-size: 0.8rem;
  font-weight: 600;
  line-height: 1;
}

/* 은행명 */
[data-theme="dark"] .subscription-card .preview-bank {
  display: inline;
  color: #94a3b8;      /* slate-400 */
  font-size: 0.85rem;
  font-weight: 500;
  line-height: 1.2;
}

/* 🌙 Dark Mode - Remove Bank Badge Style */
[data-theme="dark"] .subscription-card .preview-bank {
  background: none !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  border-radius: 0 !important;
}
/* 상품명 */
[data-theme="dark"] .subscription-card .preview-name {
  color: #e5e7eb; /* gray-200 */
  font-size: 0.95rem;
  font-weight: 500;
}

/* 금리 */
[data-theme="dark"] .subscription-card .sub-rate {
  color: #c7d2fe; /* indigo-200 */
  font-weight: 600;
}

/* 🌙 Dark Mode - Icons */
[data-theme="dark"] .icon,
[data-theme="dark"] i,
[data-theme="dark"] svg {
  color: var(--text-secondary);
  fill: var(--text-secondary);
}

[data-theme="dark"] .icon-primary {
  color: var(--primary);
  fill: var(--primary);
}

/* 🌙 Dark Mode - Empty Illustration */
[data-theme="dark"] .empty-illustration {
  opacity: 0.75;
  filter: brightness(0.9) contrast(1.1);
}

[data-theme="dark"] .login-empty {
  background: linear-gradient(
    135deg,
    #0f172a,
    #020617
  );
}

/* 🌙 Dark Mode - Subscription Card Header */
[data-theme="dark"] .subscription-card .card-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

[data-theme="dark"] .subscription-card .card-header h3 {
  color: var(--text-secondary);
  font-weight: 600;
}

/* 아이콘 */
[data-theme="dark"] .subscription-card .card-header svg,
[data-theme="dark"] .subscription-card .card-header i {
  color: #9ca3af; /* text-muted 톤 */
  fill: #9ca3af;
}

/* 🌙 Dark Mode - Subscription Item Icon (No Background) */
[data-theme="dark"] .subscription-card .preview-icon {
  background: none;
  box-shadow: none;
  border: none;
  padding: 0;
}

[data-theme="dark"] .subscription-card .preview-icon svg,
[data-theme="dark"] .subscription-card .preview-icon i {
  color: var(--text-secondary);
  fill: var(--text-secondary);
  width: 18px;
  height: 18px;
}

/* 🌙 Dark Mode - Blur Content matches Card */
[data-theme="dark"] .subscription-card .blur-content {
  background: var(--bg-card);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  opacity: 0.9;
  border: 1px solid var(--border-color);
}


/* 1. Profile Card */
.profile-card { grid-column: span 1; justify-content: center; align-items: center; text-align: center; }
.profile-content { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 12px; }

/* Logged In Style */
.avatar-circle { width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: #eff6ff; color: var(--primary); margin-bottom: 10px; }
.welcome-text { margin: 0; font-size: 1.4rem; font-weight: 800; line-height: 1.4; color: var(--text-primary); }
.highlight { 
  color: #3182F6 !important; /* var(--primary) 대신 직접 지정하거나 변수 확인 */
  font-weight: 700; 
}
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
/* ✨ 다크 모드일 때만 색상 조정 */
[data-theme="dark"] .btn-logout {
  /* 너무 하얗지 않게 더 어두운 회색으로 변경 */
  color: #bbbbbb; 
  background-color: rgba(255, 255, 255, 0.03); /* 아주 살짝 배경을 줌 (선택사항) */
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
/* [라이트/공통] 입력창 기본 스타일 */
.login-input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background-color: var(--bg-card);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

/* [다크 모드 전용] 입력창 색상 상세 조정 */
[data-theme="dark"] .login-input {
  /* 배경을 카드 색상보다 약간 더 어둡게 하여 깊이감 부여 */
  background-color: rgba(255, 255, 255, 0.05); 
  border-color: #3f3f46; /* 진한 회색 테두리 */
  color: #e5e7eb;
}

/* 플레이스홀더(힌트 텍스트) 색상 */
.login-input::placeholder {
  color: var(--text-muted);
  opacity: 0.7;
}

/* [포커스 상태] 클릭 시 강조 효과 */
.login-input:focus {
  outline: none;
  border-color: #3b82f6; /* 파란색 포인트 */
  background-color: var(--bg-card); /* 포커스 시 배경을 살짝 밝게 */
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15);
}

[data-theme="dark"] .login-input:focus {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.25);
}
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
.subscription-card {
  padding: 24px 20px 0 20px !important; /* 아래쪽(bottom) 패딩을 0으로 완전히 제거 */
  display: flex;
  flex-direction: column;
  min-height: 350px; /* 카드의 최소 높이를 확보 */
  justify-content: flex-start;
}

/* 1. 스크롤 영역: 아이템 5개 높이와 간격을 정확히 합산 */
.product-scroll-area {
  flex: 1;
  
  /* 계산식: (아이템 64px + 간격 8px) * 5개 - 마지막 간격 8px = 352px */
  /* 만약 5번째가 여전히 미세하게 가려지면 355px 정도로 살짝 늘려주세요. */
  max-height: 352px !important; 
  
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: 8px;
  
  /* 리스트 맨 아래 여백을 줘서 마지막 아이템 하단 곡선이 잘 보이지 않게 방지 */
  padding-bottom: 4px; 
}

/* 2. 개별 아이템: 높이를 64px로 딱 고정 (가장 보기 좋은 크기) */
.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  /* 높이 고정 */
  height: 64px; 
  min-height: 64px;
  
  padding: 0 16px; /* 위아래 패딩은 height가 결정하므로 0으로 둠 */
  background-color: #f9fafb;
  border-radius: 16px;
  margin-bottom: 4px; /* 아이템 사이 간격 */
  
  flex-shrink: 0; /* 중요: 아이템이 눌리지 않게 함 */
  box-sizing: border-box;
}

.preview-item:last-child {
  margin-bottom: 0;
}

/* 3. 스크롤바 최적화 (5개까지는 안 보이다가 6개부터 등장) */
.product-scroll-area::-webkit-scrollbar {
  width: 4px;
}

.product-scroll-area::-webkit-scrollbar-thumb {
  background-color: transparent;
}

/* 마우스를 올렸을 때만 스크롤바가 보이게 해서 디자인 유지 */
.product-scroll-area:hover::-webkit-scrollbar-thumb {
  background-color: #e5e8eb;
  border-radius: 10px;
}

/* 다크모드 대응 */
[data-theme="dark"] .preview-item {
  background-color: rgba(255, 255, 255, 0.05);
}

/* 4. 카드 하단에 부드러운 그라데이션 (선택 사항) */
/* 리스트가 잘리는 느낌이 들면 카드 바닥에 살짝 흰색/검은색 투명 처리를 합니다 */
.subscription-card::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 20px;
  background: linear-gradient(to top, var(--bg-card), transparent);
  pointer-events: none; /* 클릭 방해 금지 */
  border-radius: 0 0 24px 24px;
}

/* 2. 스크롤바가 실제 나타날 때만 패딩을 살짝 주어 공간 확보 */
.product-scroll-area:hover {
  padding-right: 4px;
}

/* 3. 스크롤바 디자인 (평소엔 투명하다가 호버 시에만 살짝 보이게) */
.product-scroll-area::-webkit-scrollbar {
  width: 4px; /* 스크롤바 두께 */
}

.product-scroll-area::-webkit-scrollbar-thumb {
  background-color: transparent; /* 평소엔 안 보임 */
  border-radius: 10px;
}

.product-scroll-area:hover::-webkit-scrollbar-thumb {
  background-color: #e5e8eb; /* 마우스 올렸을 때만 연한 회색으로 표시 */
}

/* 다크모드 대응 스크롤바 */
[data-theme="dark"] .product-scroll-area:hover::-webkit-scrollbar-thumb {
  background-color: rgba(255, 255, 255, 0.1);
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

/* 아이콘을 감싸는 박스의 배경과 크기 제한을 제거합니다 */
.header-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none !important; /* 배경 제거 */
  width: auto !important;      /* 고정 너비 제거 */
  height: auto !important;     /* 고정 높이 제거 */
  color: var(--text-secondary); /* 아이콘 색상을 텍스트와 맞춤 */
  padding: 0;                  /* 여백 제거 */
}

/* 아이콘 크기 조절 (원하는 경우) */
.header-icon-wrapper svg {
  width: 22px;
  height: 22px;
  stroke: var(--text-secondary); /* 다크모드 변수와 연동 */
}

/* 제목(h3)과의 간격 조정 */
.header-title-box {
  display: flex;
  align-items: center;
  gap: 8px; /* 아이콘과 글자 사이 간격 */
}

.header-title-box h3 {
  font-size: 18px;
  font-weight: 700;
  color: #191f28;
  margin: 0;
}

/* 2. 뱃지 스타일 수정 */
.count-badge {
  background-color: #4a86e8 !important; /* 항상 선명한 파란색 유지 */
  color: #ffffff !important;           /* 글자색은 항상 흰색 */
  
  /* 디자인을 위한 기본 스타일 (필요시 조정) */
  font-size: 0.75rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  box-shadow: 0 2px 5px rgba(74, 134, 232, 0.3);
}

/* 3. 제목 박스와의 간격 (혹시 제목 바로 옆에 붙이고 싶다면) */
.header-title-box {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 2. 다크모드에서 색상이 변하는 것을 방지 */
[data-theme="dark"] .count-badge {
  background-color: #4a86e8 !important; /* 다크모드에서도 파란색 고정 */
  color: #ffffff !important;           /* 다크모드에서도 흰색 고정 */
  border: none !important;             /* 혹시 생길 수 있는 테두리 제거 */
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
/* 1. 블러 컨테이너: 부모 카드의 곡률을 그대로 상속받아 삐져나오지 않게 함 */
.blur-overlay-container {
  position: relative;
  height: 100%;
  width: 100%;
  overflow: hidden;
  border-radius: inherit; /* 부모(card)의 border-radius를 그대로 따라감 */
}

/* 2. 블러 레이어: 테두리 잔상을 없애고 색상 최적화 */
.blur-content { 
  position: absolute;
  /* top, left 대신 inset 사용으로 더 정확한 밀착 */
  inset: 0; 
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: none; /* 혹시 모를 테두리 제거 */
  
  /* 블러 강도와 색상 - 라이트 모드 기본 */
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.5);
  transition: background-color 0.3s ease;
}

/* 3. ✨ 다크모드 블러 최적화: 카드 배경색과 유사한 톤으로 설정 */
[data-theme="dark"] .blur-content {
  /* 카드 배경(#1e1e1e)과 어우러지도록 어두운 톤 적용 */
  background: rgba(30, 30, 30, 0.75); 
  backdrop-filter: blur(10px); /* 다크모드에서 블러를 살짝 더 강하게 주면 고급스러움 */
}

/* 4. 뒤에 비치는 더미 아이템들 테두리 제거 (블러 너머로 보이지 않게) */
.dummy .sub-item {
  border: none !important;
  background-color: var(--bg-hover) !important;
  opacity: 0.2; /* 더 연하게 처리해서 거슬림 방지 */
}

.subscription-card:hover {
  /* 배경색과 테두리를 원래 상태로 강제 고정 */
  background-color: var(--bg-card) !important;
  border-color: var(--border-color) !important;
  
  /* 파란색 그림자(Glow) 효과 제거 (일반적인 그림자로 변경하거나 제거) */
  box-shadow: 0 8px 30px var(--shadow-color) !important; 
  
  /* 만약 카드가 위로 들리는게 싫다면 transform도 none으로 설정 가능 */
  /* transform: none !important; */
}

/* 다크모드 호버 시 */
[data-theme="dark"] .subscription-card:hover {
  background-color: rgba(49, 130, 246, 0.12);
}

/* [2] 블러 영역 - 테두리 잔상 절대 안 생기게 수정 */
.blur-overlay-container {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: inherit;
  overflow: hidden;
  /* 테두리가 없으므로 마진 필요 없음 */
  margin: 0; 
}

.blur-content {
  position: absolute;
  /* 정확히 0으로 맞춰서 테두리 효과 방지 */
  inset: 0; 
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  /* 선 생기지 않도록 강제 적용 */
  border: none !important;
  outline: none !important;
  
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.4);
  transition: background-color 0.3s ease;
}

/* 다크모드 블러 배경색 */
[data-theme="dark"] .blur-content {
  background: rgba(30, 30, 30, 0.7);
}

[data-theme="dark"] .subscription-card:hover .blur-content {
  background: rgba(30, 38, 52, 0.8);
}
/* 2. 카드 호버 시 내부 .blur-content가 파란색으로 변하는 것 방지 */
.subscription-card:hover .blur-content {
  background-color: transparent !important; /* 배경색 변화 제거 */
  color: var(--text-primary) !important;    /* 글자색 유지 */
}

/* 3. 다크모드에서 가상 요소(::before 등)로 파란 빛을 내는 경우 방어 */
[data-theme="dark"] .subscription-card:hover::before,
[data-theme="dark"] .subscription-card:hover::after {
  display: none !important;
}

/* 4. 내부의 아이콘이나 강조 텍스트가 파란색으로 변할 경우 */
.subscription-card:hover .highlight,
.subscription-card:hover i,
.subscription-card:hover span {
  color: inherit !important;
}
/* 잠금 아이콘 박스 - 여기도 테두리 제거 */
.lock-icon-box {
  width: 50px;
  height: 50px;
  background: var(--bg-hover);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  color: var(--text-secondary);
  /* 아이콘 박스 테두리도 제거하여 일체감 형성 */
  border: none !important;
}

/* 호버 시 잠금 아이콘만 색상 변경 */
.subscription-card:hover .lock-icon-box {
  color: var(--primary);
  background: var(--bg-card);
}

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
.news-link { color: inherit; text-decoration: none; }
.news-text { color: var(--text-primary); font-size: 0.95rem; line-height: 1.4; font-weight: 500; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.news-link:hover .news-text { color: var(--primary); text-decoration: underline; }
.news-ago { font-size: 0.75rem; color: var(--text-muted); white-space: nowrap; margin-top: 2px; }
/* 📰 News Card Hover - Modern */
.news-item {
  transition: 
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color 0.2s ease;
}
.news-link:hover,
.news-link:active,
.news-link:focus,
.news-link:visited {
  color: inherit;
  text-decoration: none;
}
[data-theme="dark"] .h3-title {
  color: var(--text-primary) !important;
}
.news-item:hover {
  transform: translateY(-2px);
  background-color: var(--bg-hover);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border-left: none !important;
  border-bottom: none !important;
}

[data-theme="dark"] .news-item:hover {
  background-color: rgba(255, 255, 255, 0.03);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.6);
}
.news-item:hover::before {
  opacity: 1;
}
.news-item::before {
  display: none !important;
}


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
/* 📰 News Card - Clean Hover Only */
.news-item {
  position: relative;
  border: none;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background-color 0.2s ease;
}

.news-item::before,
.news-item::after {
  display: none !important;
}

.news-item:hover {
  transform: translateY(-2px);
  background-color: var(--bg-hover);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

</style>