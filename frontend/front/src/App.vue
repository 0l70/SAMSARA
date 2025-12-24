<template>
  <header>
    <div class="top-bar">
      <div class="top-bar-content">
        <div v-if="store.isLogin" class="user-menu">
          <span class="welcome-msg">반가워요,</span>
          <RouterLink :to="{ name: 'mypage' }" class="profile-link">
            <strong>{{ store.nickname || '회원' }}</strong>님
          </RouterLink>
          <button @click="store.logOut" class="logout-btn">로그아웃</button>
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
          라고 할 때 살걸
        </RouterLink>
      </div>

      <div class="nav-right">
        
        <div class="nav-group">
          <button 
            class="nav-btn" 
            :class="{ 'active': isGroupActive(['products', 'BankView']) }"
          >
            금융 상품 <span class="arrow">▼</span>
          </button>
          
          <div class="dropdown-menu">
            <RouterLink :to="{ name: 'products' }" class="dropdown-item">
              🏦 예적금 비교
            </RouterLink>
            <RouterLink :to="{ name: 'subscription-list' }" class="dropdown-item">
              📑 가입 리스트
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

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router' // useRoute 추가
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const route = useRoute() // 현재 페이지 정보를 담고 있는 객체

// 현재 페이지 이름(route.name)이, 지정한 그룹 목록(names)에 포함되는지 확인하는 함수
const isGroupActive = (names) => {
  return names.includes(route.name)
}
</script>

<style>
/* 전역 설정 */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, "Noto Sans KR", sans-serif;
  color: #191f28;
  background-color: #f2f4f6;
}
</style>

<style scoped>
/* 헤더 기본 스타일 */
header {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  box-shadow: 0 1px 0 rgba(0,0,0,0.05);
}

.top-bar {
  background-color: #fff;
  border-bottom: 1px solid #f2f4f6;
}

.top-bar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 10px 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: 13px;
  color: #8b95a1;
}

.top-bar a { text-decoration: none; color: #8b95a1; transition: color 0.2s; margin-left: 16px; }
.top-bar a:hover { color: #3182f6; }
.profile-link strong { color: #3182f6; font-weight: 700; }
.logout-btn { background: none; border: none; cursor: pointer; font-size: 13px; color: #8b95a1; margin-left: 16px; padding: 0; transition: color 0.2s; }
.logout-btn:hover { color: #e11d48; text-decoration: underline; }
.divider { display: inline-block; width: 1px; height: 10px; background: #e5e8eb; margin: 0 10px; }

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
  font-size: 22px;
  font-weight: 800;
  color: #191f28;
  text-decoration: none;
  letter-spacing: -0.5px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 8px;
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
  font-size: 16px;
  font-weight: 600;
  color: #4e5968;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
  text-decoration: none;
}

.arrow { font-size: 10px; color: #b0b8c1; transition: transform 0.2s, color 0.2s; }

/* 1. 호버(Hover) 효과: 마우스 올렸을 때 */
.nav-group:hover .nav-btn, 
.single-link:hover { 
  background-color: rgba(2, 32, 71, 0.05);
  color: #333d4b; 
}
.nav-group:hover .arrow { transform: rotate(180deg); color: #333d4b; }

/* 2. 활성화(Active) 효과: 현재 페이지가 그룹에 속할 때 
  (여기가 핵심입니다!) 
*/
.nav-btn.active, 
.router-link-active.single-link {
  color: #3182f6; /* 파란색 글씨 */
  background-color: rgba(49, 130, 246, 0.08); /* 연한 파란색 배경 */
}

/* 상위 버튼이 활성화되면 화살표 색상도 변경 */
.nav-btn.active .arrow {
  color: #3182f6; 
}

/* 드롭다운 메뉴 */
.dropdown-menu {
  position: absolute;
  top: 90%;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background-color: white;
  min-width: 220px;
  border-radius: 16px;
  padding: 8px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.08), 0 2px 10px rgba(0,0,0,0.03);
  border: 1px solid rgba(0,0,0,0.05);
  opacity: 0;
  visibility: hidden;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
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
  color: #4e5968;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  margin-bottom: 2px;
  transition: background-color 0.2s, color 0.2s;
}

/* 현재 페이지와 일치하는 드롭다운 아이템은 글씨를 파랗게 */
.router-link-active.dropdown-item {
  color: #3182f6;
  font-weight: 700;
  background-color: #f2f4f6;
}

.dropdown-item:hover {
  background-color: #f2f4f6;
  color: #3182f6;
}

@media (max-width: 768px) {
  .main-nav { padding: 0 16px; }
  .logo { font-size: 18px; }
  .nav-btn, .single-link { font-size: 14px; padding: 8px 10px; }
  .nav-right { gap: 2px; }
}
</style>