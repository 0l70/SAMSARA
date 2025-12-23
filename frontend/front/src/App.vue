<template>
  <header>
    <div class="top-bar">
      <div v-if="store.isLogin" class="user-menu">
        <span class="welcome-msg">환영합니다,</span>
        <RouterLink :to="{ name: 'mypage' }" class="profile-link">
          <strong>{{ store.nickname || '회원' }}</strong>님
        </RouterLink>
        <button @click="store.logOut" class="logout-btn">로그아웃</button>
      </div>
      <div v-else class="auth-links">
        <RouterLink :to="{ name: 'login' }">로그인</RouterLink>
        <span class="divider">|</span>
        <RouterLink :to="{ name: 'signup' }">회원가입</RouterLink>
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
          <button class="nav-btn">
            금융 상품 <span class="arrow">▼</span>
          </button>
          <div class="dropdown-menu">
            <RouterLink :to="{ name: 'products' }" class="dropdown-item">
              🏦 예적금 비교
            </RouterLink>
            <RouterLink :to="{ name: 'BankView' }" class="dropdown-item">
              📍 주변 은행 찾기
            </RouterLink>
          </div>
        </div>

        <div class="nav-group">
          <button class="nav-btn">
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

        <RouterLink :to="{ name: 'articles' }" class="nav-item single-link">
          게시판
        </RouterLink>

      </div>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
</script>

<style scoped>
/* =========================================
   기본 레이아웃
   ========================================= */
header {
  width: 100%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05); /* 더 부드러운 그림자 */
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.95); /* 살짝 투명해서 고급짐 */
  backdrop-filter: blur(10px); /* 블러 효과 */
}

/* 상단 유틸리티 바 */
.top-bar {
  background-color: #f8f9fa;
  padding: 8px 20px;
  font-size: 13px;
  border-bottom: 1px solid #edf2f7;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  color: #666;
}
.top-bar a { text-decoration: none; color: #666; transition: 0.2s; margin-left: 15px; }
.top-bar a:hover { color: #42b983; }
.logout-btn { background: none; border: none; cursor: pointer; font-size: 13px; color: #666; margin-left: 15px; }
.divider { margin: 0 10px; color: #ddd; }

/* 메인 네비게이션 컨테이너 */
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
  height: 70px; /* 높이 고정 */
  max-width: 1280px;
  margin: 0 auto;
}

/* 로고 */
.logo {
  font-size: 24px;
  font-weight: 800;
  color: #2c3e50;
  text-decoration: none;
  letter-spacing: -0.5px;
}

/* =========================================
   ★ 드롭다운 메뉴 스타일 (핵심)
   ========================================= */
.nav-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* 1. 그룹 컨테이너 */
.nav-group {
  position: relative; /* 드롭다운의 기준점 */
  height: 70px; /* 네비게이션 높이와 맞춤 */
  display: flex;
  align-items: center;
}

/* 2. 상위 메뉴 버튼 */
.nav-btn {
  background: none;
  border: none;
  font-size: 17px;
  font-weight: 600;
  color: #333;
  cursor: pointer;
  padding: 0 15px;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: color 0.3s;
}
.arrow { font-size: 10px; transition: transform 0.3s; color: #999; }

/* 마우스 올렸을 때 효과 */
.nav-group:hover .nav-btn { color: #42b983; }
.nav-group:hover .arrow { transform: rotate(180deg); color: #42b983; }

/* 3. 드롭다운 박스 (숨겨져 있다가 나옴) */
.dropdown-menu {
  position: absolute;
  top: 100%; /* 버튼 바로 아래 */
  left: 50%;
  transform: translateX(-50%) translateY(10px); /* 중앙 정렬 + 약간 아래 시작 */
  background-color: white;
  min-width: 200px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border-radius: 12px;
  padding: 10px 0;
  
  /* 숨김 처리 */
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
}

/* 마우스 올리면 드롭다운 등장 */
.nav-group:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) translateY(0); /* 제자리로 올라옴 */
}

/* 4. 드롭다운 내부 아이템 */
.dropdown-item {
  display: block;
  padding: 12px 20px;
  text-decoration: none;
  color: #555;
  font-size: 15px;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #42b983;
}

/* 단일 링크 (게시판) 스타일 */
.single-link {
  text-decoration: none;
  color: #333;
  font-weight: 600;
  font-size: 17px;
  padding: 0 15px;
  transition: color 0.3s;
}
.single-link:hover { color: #42b983; }
.router-link-active.single-link { color: #42b983; }

/* 반응형 (화면 작아지면 여백 조정) */
@media (max-width: 768px) {
  .main-nav { padding: 0 15px; }
  .logo { font-size: 20px; }
  .nav-btn, .single-link { font-size: 15px; padding: 0 8px; }
}
</style>