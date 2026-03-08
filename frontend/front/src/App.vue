<template>
  <div class="app-wrapper">
    
    <header>
      <div class="top-bar">
        <div class="top-bar-content">
          <div v-if="authStore.isLogin" class="user-menu">
            <span class="welcome-msg">반가워요,</span>
            <RouterLink :to="{ name: 'mypage' }" class="profile-link">
              <strong>{{ authStore.nickname || '회원' }}</strong>님
            </RouterLink>
            <button @click="authStore.logOut" class="logout-btn">로그아웃</button>
          </div>
          <div v-else class="auth-links">
            <RouterLink :to="{ name: 'login' }">로그인</RouterLink>
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
            <button class="nav-btn" :class="{ 'active': isGroupActive(['products', 'BankView', 'subscription-list']) }">
              금융 상품 <span class="arrow">▼</span>
            </button>
            <div class="dropdown-menu">
              <RouterLink :to="{ name: 'products' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
                예적금 비교
              </RouterLink>
              <RouterLink :to="{ name: 'subscription-list' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>
                가입 리스트
              </RouterLink>
              <RouterLink :to="{ name: 'BankView' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
                주변 은행 찾기
              </RouterLink>
            </div>
          </div>

          <div class="nav-group">
            <button class="nav-btn" :class="{ 'active': isGroupActive(['exchange', 'gold', 'youtube-search']) }">
              투자/분석 <span class="arrow">▼</span>
            </button>
            <div class="dropdown-menu">
              <RouterLink :to="{ name: 'exchange' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg>
                환율 계산기
              </RouterLink>
              <RouterLink :to="{ name: 'gold' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"></circle><path d="M18.09 10.37A6 6 0 1 1 10.34 18"></path><path d="M7 6h1v4"></path><path d="M17 17v-4h1"></path></svg>
                금/은 시세
              </RouterLink>
              <RouterLink :to="{ name: 'youtube-search' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                금융 영상 검색
              </RouterLink>
            </div>
          </div>

          <div class="nav-group">
            <button class="nav-btn" :class="{ 'active': isGroupActive(['test', 'chatbot']) }">
              AI 맞춤 금융 비서 <span class="arrow">▼</span>
            </button>
            <div class="dropdown-menu">
              <RouterLink :to="{ name: 'test' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                금융 MBTI 테스트
              </RouterLink>
              <RouterLink :to="{ name: 'chatbot' }" class="dropdown-item">
                <svg class="nav-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>
                나만의 비서 AI 챗봇
              </RouterLink>
            </div>
          </div>

          <RouterLink :to="{ name: 'articles' }" class="nav-item single-link">
            게시판
          </RouterLink>

          <button 
            @click="themeStore.toggleTheme" 
            class="theme-toggle-btn-modern" 
            :title="themeStore.isDark ? '라이트 모드로 전환' : '다크 모드로 전환'"
            aria-label="테마 변경"
          >
            <transition name="rotate" mode="out-in">
              <svg 
                v-if="themeStore.isDark" 
                key="moon" 
                class="theme-icon moon-icon" 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              >
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
              </svg>

              <svg 
                v-else 
                key="sun" 
                class="theme-icon sun-icon" 
                xmlns="http://www.w3.org/2000/svg" 
                viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              >
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
              </svg>
            </transition>
          </button>
        
        </div>
      </nav>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const route = useRoute()

const isGroupActive = (names) => {
  return names.includes(route.name)
}
</script>

<style>
/* 폰트 설정 */
@font-face {
    font-family: 'PartialSans';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2307-1@1.1/PartialSansKR-Regular.woff2') format('woff2');
    font-weight: normal; font-style: normal; font-display: swap;
}

/* 글로벌 변수 설정 */
:root {
  /* 라이트 모드 */
  --bg-body: #f2f4f6; --bg-header: rgba(255, 255, 255, 0.85); --bg-card: #ffffff;
  --bg-hover: #f2f4f6; --bg-badge: #e3f2fd; --text-primary: #191f28;
  --text-secondary: #4e5968; --text-muted: #8b95a1; --border-color: #e5e8eb;
  --primary-color: #3182f6; --shadow-color: rgba(0,0,0,0.08);
}

[data-theme="dark"] {
  /* 다크 모드 */
  --bg-body: #121212; --bg-header: rgba(30, 30, 30, 0.85); --bg-card: #1e1e1e;
  --bg-hover: #2c2c2c; --bg-badge: #1a2736; --text-primary: #e0e0e0;
  --text-secondary: #b0b8c1; --text-muted: #6b7684; --border-color: #333333;
  --primary-color: #5c9dff; --shadow-color: rgba(0,0,0,0.5);
}

body {
  margin: 0; padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, "Noto Sans KR", sans-serif;
  color: var(--text-primary); background-color: var(--bg-body);
  overflow-y: auto; transition: background-color 0.3s ease, color 0.3s ease;
}
#app { min-height: 100vh; }
</style>

<style scoped>
/* 레이아웃 구조 */
.app-wrapper { display: flex; flex-direction: column; min-height: 100vh; }
.main-content { flex: 1; width: 100%; position: relative; }

/* 헤더 스타일 */
header {
  width: 100%; position: sticky; top: 0; z-index: 1000;
  background-color: var(--bg-header); backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 var(--shadow-color); flex-shrink: 0; transition: background-color 0.3s;
}

/* 상단 유틸리티 바 */
.top-bar { background-color: var(--bg-header); border-bottom: 1px solid var(--border-color); }
.top-bar-content {
  max-width: 1200px; margin: 0 auto; padding: 6px 20px;
  display: flex; justify-content: flex-end;
  align-items: center; font-size: 13px; color: var(--text-muted);
}
.top-bar a { text-decoration: none; color: var(--text-muted); transition: color 0.2s; margin-left: 16px; }
.top-bar a:hover { color: var(--primary-color); }
.profile-link strong { color: var(--primary-color); font-weight: 700; }
.logout-btn { background: none; border: none; cursor: pointer; font-size: 13px; color: var(--text-muted); margin-left: 16px; padding: 0; transition: color 0.2s; }
.logout-btn:hover { color: #e11d48; text-decoration: underline; }

/* 메인 네비게이션 컨테이너 */
.main-nav { display: flex; justify-content: space-between; align-items: center; height: 64px; max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.logo { font-family: 'PartialSans', sans-serif; font-size: 36px; font-weight: normal; color: var(--text-primary); text-decoration: none; letter-spacing: -0.5px; display: flex; align-items: center; }
.nav-right { display: flex; align-items: center; gap: 8px; }
.nav-group { position: relative; height: 64px; display: flex; align-items: center; }

/* 네비게이션 버튼 & 링크 공통 */
.nav-btn, .single-link { background: none; border: none; font-size: 16px; font-weight: 600; color: var(--text-secondary); padding: 10px 14px; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 4px; transition: all 0.2s ease; text-decoration: none; }
.arrow { font-size: 10px; color: var(--text-muted); transition: transform 0.2s, color 0.2s; }
.nav-group:hover .nav-btn, .single-link:hover { background-color: var(--bg-hover); color: var(--text-primary); }
.nav-group:hover .arrow { transform: rotate(180deg); color: var(--text-primary); }
.nav-btn.active, .router-link-active.single-link { color: var(--primary-color); background-color: rgba(49, 130, 246, 0.08); }
.nav-btn.active .arrow { color: var(--primary-color); }

/* 드롭다운 메뉴 */
.dropdown-menu { 
  position: absolute; top: 90%; left: 50%; transform: translateX(-50%) translateY(10px); 
  background-color: var(--bg-card); min-width: 220px; border-radius: 16px; padding: 8px; 
  box-shadow: 0 10px 40px var(--shadow-color), 0 2px 10px rgba(0,0,0,0.03); 
  border: 1px solid var(--border-color); 
  opacity: 0; visibility: hidden; 
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1); z-index: 2000; 
}
.nav-group:hover .dropdown-menu { opacity: 1; visibility: visible; top: 100%; transform: translateX(-50%) translateY(0); }

/* 드롭다운 아이템 */
.dropdown-item { 
  display: flex; 
  align-items: center; 
  gap: 12px; 
  padding: 12px 16px; 
  text-decoration: none; 
  color: var(--text-secondary); font-size: 15px; font-weight: 500; 
  border-radius: 10px; margin-bottom: 2px; 
  transition: background-color 0.2s, color 0.2s; 
}

/* 드롭다운 내부 SVG 아이콘 */
.nav-icon {
  width: 18px; 
  height: 18px; 
  stroke-width: 2px;
  flex-shrink: 0;
  color: inherit; 
}

.router-link-active.dropdown-item { color: var(--primary-color); font-weight: 700; background-color: var(--bg-hover); }
.dropdown-item:hover { background-color: var(--bg-hover); color: var(--primary-color); }

/* ✨ 테마 토글 버튼 스타일 (SVG 대응) */
.theme-toggle-btn-modern {
  background: none; border: none; cursor: pointer; padding: 8px; margin-left: 12px; 
  border-radius: 50%; display: flex; align-items: center; justify-content: center; 
  color: var(--text-secondary); transition: all 0.3s ease;
}
.theme-toggle-btn-modern:hover { background-color: var(--bg-hover); color: var(--primary-color); transform: rotate(15deg); }

/* 테마 아이콘 공통 */
.theme-icon { width: 20px; height: 20px; stroke-width: 2px; display: block; }

/* 호버 시 아이콘 색상 효과 */
.theme-toggle-btn-modern:hover .sun-icon { color: #f59e0b; fill: rgba(245, 158, 11, 0.1); }
.theme-toggle-btn-modern:hover .moon-icon { color: #6366f1; fill: rgba(99, 102, 241, 0.1); }

/* 아이콘 회전 애니메이션 */
.rotate-enter-active, .rotate-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.rotate-enter-from { opacity: 0; transform: rotate(-90deg) scale(0.5); }
.rotate-leave-to { opacity: 0; transform: rotate(90deg) scale(0.5); }

@media (max-width: 768px) {
  .theme-toggle-btn-modern { margin-left: 8px; padding: 6px; }
  .theme-icon { font-size: 20px; }
  .main-nav { padding: 0 16px; }
  .logo { font-size: 22px; }
  .nav-btn, .single-link { font-size: 14px; padding: 8px 10px; }
  .nav-right { gap: 4px; }
}
</style>

<style>
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(15px);
}

.page-fade-leave-to {
  opacity: 0;
}
html, body {
  margin: 0;
  padding: 0;
  /* 변수가 로드되기 전에도 하얀색(또는 다크모드 배경색)이 보이도록 설정 */
  background-color: #f2f4f6; 
}

/* 다크모드일 때 초기 배경색 */
[data-theme="dark"] body {
  background-color: #121212;
}

/* 만약 app-wrapper에 파란색 배경이 들어가 있다면 제거 */
.app-wrapper {
  background-color: var(--bg-body); /* 파란색이 아닌 배경색 변수 사용 */
  min-height: 100vh;
}
</style>