<template>
  <div class="app-wrapper">
    
    <header>
      <div class="top-bar">
        <div class="top-bar-content">
          <button @click="themeStore.toggleTheme" class="theme-toggle-btn" title="테마 변경">
            <span v-if="themeStore.isDark">🌙 Dark</span>
            <span v-else>☀️ Light</span>
          </button>

          <div v-if="authStore.isLogin" class="user-menu">
            <span class="welcome-msg">반가워요,</span>
            <RouterLink :to="{ name: 'mypage' }" class="profile-link">
              <strong>{{ authStore.nickname || '회원' }}</strong>님
            </RouterLink>
            <button @click="authStore.logOut" class="logout-btn">로그아웃</button>
          </div>
          <div v-else class="auth-links">
            <RouterLink :to="{ name: 'login' }">로그인</RouterLink>
            <span class="divider"></span>
            <RouterLink :to="{ name: 'signup' }">회원가입</RouterLink>
          </div>
        </div>
      </div>

      <nav class="main-nav">
        <div class="nav-left">
          <RouterLink :to="{ name: 'home' }" class="logo">
            삼사라
          </RouterLink>
        </div>

        <div class="nav-right">
          <div class="nav-group">
            <button 
              class="nav-btn" 
              :class="{ 'active': isGroupActive(['products', 'BankView', 'subscription-list']) }"
            >
              금융 상품 <span class="arrow">▼</span>
            </button>
            <div class="dropdown-menu">
              <RouterLink :to="{ name: 'products' }" class="dropdown-item">
                🏦 예적금 비교
              </RouterLink>
              <RouterLink :to="{ name: 'subscription-list' }" class="dropdown-item">
                📝 가입 리스트
              </RouterLink>
              <RouterLink :to="{ name: 'BankView' }" class="dropdown-item">
                📍 주변 은행 찾기
              </RouterLink>
            </div>
          </div>

          <div class="nav-group">
            <button 
              class="nav-btn" 
              :class="{ 'active': isGroupActive(['exchange', 'gold', 'youtube-search']) }"
            >
              투자/분석 <span class="arrow">▼</span>
            </button>
            
            <div class="dropdown-menu">
              <RouterLink :to="{ name: 'exchange' }" class="dropdown-item">
                💱 환율 계산기
              </RouterLink>
              <RouterLink :to="{ name: 'gold' }" class="dropdown-item">
                🥇 금/현물 시세
              </RouterLink>
              <RouterLink :to="{ name: 'youtube-search' }" class="dropdown-item">
                📺 금융 영상 검색
              </RouterLink>
            </div>
          </div>

          <div class="nav-group">
            <button 
              class="nav-btn" 
              :class="{ 'active': isGroupActive(['test', 'chatbot']) }"
            >
              AI 맞춤 금융 비서 <span class="arrow">▼</span>
            </button>
            
            <div class="dropdown-menu">
              <RouterLink :to="{ name: 'test' }" class="dropdown-item">
                💰 금융 MBTI 테스트
              </RouterLink>
              <RouterLink :to="{ name: 'chatbot' }" class="dropdown-item">
                🤖 나만의 비서 AI 챗봇
              </RouterLink>
            </div>
          </div>

          <RouterLink :to="{ name: 'articles' }" class="nav-item single-link">
            게시판
          </RouterLink>
        
        </div>
      </nav>
    </header>

    <main class="main-content">
      <RouterView />
    </main>

  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme' // ✨ 테마 스토어 import

const authStore = useAuthStore()
const themeStore = useThemeStore() // ✨ 테마 스토어 사용
const route = useRoute()

const isGroupActive = (names) => {
  return names.includes(route.name)
}
</script>

<style>
/* ========================
   1. 전역 폰트 설정 (기존 유지)
   ======================== */
@font-face {
    font-family: 'PartialSans';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2307-1@1.1/PartialSansKR-Regular.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
}

/* ========================
   2. 다크 모드 변수 선언 (새로 추가)
   ======================== */
:root {
  /* 라이트 모드 (기본값) */
  --bg-body: #f2f4f6;
  --bg-header: rgba(255, 255, 255, 0.85);
  --bg-card: #ffffff;
  --bg-hover: #f2f4f6; /* 연한 회색 */
  --bg-badge: #e3f2fd;
  
  --text-primary: #191f28;
  --text-secondary: #4e5968;
  --text-muted: #8b95a1;
  
  --border-color: #e5e8eb;
  --primary-color: #3182f6;
  --shadow-color: rgba(0,0,0,0.08);
}

[data-theme="dark"] {
  /* 다크 모드 (오버라이드) */
  --bg-body: #121212;
  --bg-header: rgba(30, 30, 30, 0.85);
  --bg-card: #1e1e1e;
  --bg-hover: #2c2c2c; /* 조금 밝은 회색 */
  --bg-badge: #1a2736;
  
  --text-primary: #e0e0e0;
  --text-secondary: #b0b8c1;
  --text-muted: #6b7684;
  
  --border-color: #333333;
  --primary-color: #5c9dff; /* 다크모드에선 파란색을 살짝 밝게 */
  --shadow-color: rgba(0,0,0,0.5);
}

/* ========================
   3. Body 기본 스타일 적용
   ======================== */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, "Noto Sans KR", sans-serif;
  color: var(--text-primary); /* 변수 적용 */
  background-color: var(--bg-body); /* 변수 적용 */
  overflow-y: auto;
  transition: background-color 0.3s ease, color 0.3s ease;
}

#app {
  min-height: 100vh;
}
</style>

<style scoped>
/* ✨ 핵심 레이아웃 설정 (기존 유지) */
.app-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  width: 100%;
  position: relative;
}

/* 헤더 스타일 (변수 적용) */
header {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--bg-header); /* ✨ 변수 */
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 var(--shadow-color); /* ✨ 변수 */
  flex-shrink: 0;
  transition: background-color 0.3s;
}

.top-bar {
  background-color: var(--bg-header); /* ✨ 변수 */
  border-bottom: 1px solid var(--border-color); /* ✨ 변수 */
}

.top-bar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1px 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 13px;
  color: var(--text-muted); /* ✨ 변수 */
}

/* ✨ 테마 토글 버튼 스타일 */
.theme-toggle-btn {
  margin-right: auto; /* 왼쪽 끝으로 정렬 */
  background: none;
  border: 1px solid var(--border-color);
  padding: 4px 10px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 12px;
  color: var(--text-secondary);
  transition: all 0.2s;
}
.theme-toggle-btn:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.top-bar a { text-decoration: none; color: var(--text-muted); transition: color 0.2s; margin-left: 16px; }
.top-bar a:hover { color: var(--primary-color); }
.profile-link strong { color: var(--primary-color); font-weight: 700; }
.logout-btn { background: none; border: none; cursor: pointer; font-size: 13px; color: var(--text-muted); margin-left: 16px; padding: 0; transition: color 0.2s; }
.logout-btn:hover { color: #e11d48; text-decoration: underline; }
.divider { display: inline-block; width: 1px; height: 10px; background: var(--border-color); margin: 0 10px; }

/* 메인 네비게이션 */
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  font-family: 'PartialSans', sans-serif;
  font-size: 40px;
  font-weight: normal;
  color: var(--text-primary); /* ✨ 변수 */
  text-decoration: none;
  letter-spacing: -0.5px;
  display: flex;
  align-items: center;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 30px;
}

.nav-group {
  position: relative;
  height: 64px;
  display: flex;
  align-items: center;
}

/* 메뉴 버튼 공통 스타일 */
.nav-btn, .single-link {
  background: none;
  border: none;
  font-size: 18px; 
  font-weight: 600;
  color: var(--text-secondary); /* ✨ 변수 */
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
  text-decoration: none;
}

.arrow { font-size: 10px; color: var(--text-muted); transition: transform 0.2s, color 0.2s; }

.nav-group:hover .nav-btn, 
.single-link:hover { 
  background-color: var(--bg-hover); /* ✨ 변수 */
  color: var(--text-primary); 
}
.nav-group:hover .arrow { transform: rotate(180deg); color: var(--text-primary); }

.nav-btn.active, 
.router-link-active.single-link {
  color: var(--primary-color);
  background-color: rgba(49, 130, 246, 0.08); /* 파란색 배경은 투명도 유지 */
}

.nav-btn.active .arrow {
  color: var(--primary-color); 
}

/* 드롭다운 메뉴 */
.dropdown-menu {
  position: absolute;
  top: 90%;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background-color: var(--bg-card); /* ✨ 변수 */
  min-width: 220px;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 10px 40px var(--shadow-color), 0 2px 10px rgba(0,0,0,0.03); /* ✨ 변수 */
  border: 1px solid var(--border-color); /* ✨ 변수 */
  opacity: 0;
  visibility: hidden;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
  z-index: 2000; /* 드롭다운이 위에 오도록 */
}

.nav-group:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  top: 100%;
  transform: translateX(-50%) translateY(0);
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  text-decoration: none;
  color: var(--text-secondary); /* ✨ 변수 */
  font-size: 16px;
  font-weight: 500;
  border-radius: 10px;
  margin-bottom: 2px;
  transition: background-color 0.2s, color 0.2s;
}

.router-link-active.dropdown-item {
  color: var(--primary-color);
  font-weight: 700;
  background-color: var(--bg-hover); /* ✨ 변수 */
}

.dropdown-item:hover {
  background-color: var(--bg-hover); /* ✨ 변수 */
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .main-nav { padding: 0 16px; }
  .logo { font-size: 22px; }
  .nav-btn, .single-link { font-size: 14px; padding: 8px 10px; }
  .nav-right { gap: 2px; }
}
</style>