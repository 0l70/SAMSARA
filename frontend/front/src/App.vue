<template>
  <header>
    <div class="top-bar">
      <div v-if="store.isLogin" class="user-menu">
        <span class="welcome-msg">환영합니다,</span>
        <RouterLink :to="{ name: 'mypage' }" class="profile-link">
          <strong>{{ store.nickname || '회원' }}</strong>님!
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
        <RouterLink :to="{ name: 'articles' }" class="logo">
          라고 할 때 살걸
        </RouterLink>
      </div>

      <div class="nav-right">
        <RouterLink :to="{ name: 'products' }" class="nav-item">금융상품 비교</RouterLink>
        <RouterLink :to="{ name: 'exchange' }" class="nav-item">환율 계산기</RouterLink>
        <RouterLink :to="{ name: 'gold' }"class="nav-item">현물 시세</RouterLink>
        <RouterLink :to="{ name: 'BankView' }" class="nav-item">은행 찾기</RouterLink>
        <RouterLink :to="{ name: 'articles' }" class="nav-item">게시판</RouterLink>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // ★ 스토어 경로 확인

const store = useAuthStore()
</script>

<style scoped>
/* 헤더 전체 고정 및 그림자 */
header {
  width: 100%;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: white;
}

/* 1. 상단 유틸리티 바 */
.top-bar {
  background-color: #f8f9fa;
  padding: 3px 20px; 
  font-size: 14px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

/* 링크 공통 스타일 */
.top-bar a {
  text-decoration: none;
  color: #666;
  transition: color 0.2s;
  margin-left: 10px;
}
.top-bar a:hover {
  color: #42b983;
  text-decoration: underline;
}

/* 로그인 상태 요소들 */
.user-menu { display: flex; align-items: center; }
.welcome-msg { 
  color: #555; 
  margin-right: 2px; /* 2px 또는 아예 붙이고 싶으면 0으로 변경 */
}
.profile-link strong { color: #333; font-weight: 700; }
.profile-link:hover strong { color: #3b82f6; }
.logout-btn {
  background: none; border: none; cursor: pointer;
  font-size: 13px; color: #666; margin-left: 10px; padding: 0;
}
.logout-btn:hover { color: #ef4444; text-decoration: underline; }

/* 비로그인 상태 요소들 */
.auth-links { display: flex; align-items: center; }
.divider { margin: 0 10px; color: #ccc; font-size: 10px; }


/* 2. 메인 내비게이션 */
.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: white;
  max-width: 1200px;
  margin: 0 auto;
}

/* 로고 */
.logo {
  font-size: 26px;
  font-weight: 800;
  color: #2c3e50;
  text-decoration: none;
  font-family: 'Arial', sans-serif;
  letter-spacing: -1px;
}

/* 메뉴 리스트 */
.nav-right { display: flex; gap: 25px; }
.nav-item {
  text-decoration: none;
  color: #333;
  font-weight: 600;
  font-size: 17px;
  padding: 5px 0;
  position: relative;
  transition: color 0.3s;
}
.nav-item:hover { color: #42b983; }

/* 활성화된 메뉴 밑줄 효과 */
.router-link-active.nav-item { color: #42b983; }
.router-link-active.nav-item::after {
  content: '';
  position: absolute; bottom: 0; left: 0;
  width: 100%; height: 3px; background-color: #42b983; border-radius: 2px;
}
</style>