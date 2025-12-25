<template>
  <div class="page-container">
    <div class="board-wrapper">
      
      <div class="header-group">
        <div class="text-group">
          <span class="badge">Community</span>
            <h1>자유 게시판</h1>
          <p class="subtitle">다양한 금융 이야기를 자유롭게 나눠보세요.</p>
        </div>
        <a href="#" class="btn-create" @click.prevent="goCreateArticle">
          글쓰기
        </a>
      </div>

      <div class="table-card">
        <table class="article-table">
          <thead>
            <tr>
              <th width="8%">번호</th>
              <th width="55%">제목</th>
              <th width="17%">작성자</th>
              <th width="20%">작성일</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(article, index) in store.articles" :key="article.id" class="data-row">
              <td class="col-id">{{ index + 1 }}</td>
              <td class="col-title">
                <RouterLink :to="{ name: 'article-detail', params: { id: article.id }}">
                  {{ article.title }}
                </RouterLink>
              </td>
              <td class="col-author">{{ article.username }}</td>
              <td class="col-date">{{ article.created_at?.substring(0, 10) }}</td>
            </tr>
          </tbody>
        </table>
        
        <div v-if="store.articles && store.articles.length === 0" class="empty-state">
          <div class="empty-icon-box">
            <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="50" cy="50" r="40" fill="url(#paint0_linear_empty)" fill-opacity="0.1"/>
              
              <rect x="30" y="25" width="40" height="50" rx="4" fill="white" stroke="#E5E7EB" stroke-width="2"/>
              
              <path d="M38 38H62" stroke="#F3F4F6" stroke-width="3" stroke-linecap="round"/>
              <path d="M38 48H62" stroke="#F3F4F6" stroke-width="3" stroke-linecap="round"/>
              <path d="M38 58H50" stroke="#F3F4F6" stroke-width="3" stroke-linecap="round"/>

              <g class="floating-pen">
                <path d="M68 68L78 78" stroke="#3B82F6" stroke-width="4" stroke-linecap="round"/>
                <path d="M68 68L58 58L62 54L72 64L68 68Z" fill="#3B82F6"/>
                <path d="M58 58L55 61L57 63L58 58Z" fill="#1D4ED8"/>
              </g>

              <path d="M75 30L77 34L81 36L77 38L75 42L73 38L69 36L73 34L75 30Z" fill="#F59E0B"/>

              <defs>
                <linearGradient id="paint0_linear_empty" x1="50" y1="10" x2="50" y2="90" gradientUnits="userSpaceOnUse">
                  <stop stop-color="#3B82F6"/>
                  <stop offset="1" stop-color="#8B5CF6"/>
                </linearGradient>
              </defs>
            </svg>
          </div>

          <p>아직 작성된 게시글이 없습니다.<br>첫 번째 글의 주인공이 되어보세요!</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth' 

const store = useArticleStore()
const authStore = useAuthStore() 
const router = useRouter()

const goCreateArticle = () => {
  if (authStore.token) {
    router.push({ name: 'article-create' }) 
  } else {
    alert('로그인이 필요한 서비스입니다.')
    router.push({ name: 'login' }) 
  }
}

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css");

/* 1. 기본 레이아웃 */
.page-container {
  background-color: var(--bg-body);
  min-height: 100vh;
  padding: 60px 20px;
  font-family: 'Pretendard', sans-serif;
  transition: background-color 0.3s ease;
}

.board-wrapper { max-width: 1000px; margin: 0 auto; }

/* 2. 헤더 영역 */
.header-group {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
}

.text-group { display: flex; flex-direction: column; }

.badge {
  background-color: var(--bg-badge);
  color: #4a86e8;
  font-size: 0.8rem;
  font-weight: 700;
  padding: 5px 10px;
  border-radius: 20px;
  margin-bottom: 8px;
  width: fit-content;
}

.header-group h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 5px 0;
  letter-spacing: -1px;
}

.subtitle { color: var(--text-secondary); font-size: 1rem; margin: 0; }

/* 3. 버튼 스타일 */
.btn-create {
  background-color: #4a86e8; 
  color: white;
  padding: 12px 24px;
  text-decoration: none;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 10px rgba(74, 134, 232, 0.2);
  transition: all 0.2s ease;
}

.btn-create:hover {
  filter: brightness(0.9);
  transform: translateY(-2px);
}

/* 4. 테이블 카드 스타일 */
.table-card {
  background: var(--bg-card);
  border-radius: 24px;
  box-shadow: 0 10px 30px var(--shadow-color);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: background-color 0.3s ease, border-color 0.3s ease;
  min-height: 400px; /* 빈 상태일 때도 최소 높이 유지 */
  display: flex;
  flex-direction: column;
}

.article-table { width: 100%; border-collapse: collapse; }

.article-table th {
  background-color: var(--bg-body); 
  padding: 18px;
  text-align: center;
  color: var(--text-secondary);
  font-weight: 700;
  font-size: 0.95rem;
  border-bottom: 1px solid var(--border-color);
}

.article-table td {
  padding: 20px 18px;
  border-bottom: 1px solid var(--border-color);
  text-align: center;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.data-row { transition: background-color 0.2s; }
.data-row:hover { background-color: var(--bg-hover); }
.data-row:last-child td { border-bottom: none; }

.col-id { color: var(--text-muted); font-weight: 500; }
.col-title { text-align: left !important; padding-left: 30px; }
.col-title a {
  text-decoration: none;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1.05rem;
  display: block;
  transition: color 0.2s;
}
.col-title a:hover { color: #4a86e8; } 

.col-author { color: var(--text-secondary); font-weight: 500; }
.col-date { color: var(--text-muted); font-size: 0.85rem; letter-spacing: 0; }

/* 5. 빈 상태 (Empty State) 스타일 & 애니메이션 */
.empty-state { 
  flex: 1; /* 테이블 아래 남은 공간 채우기 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon-box { margin-bottom: 20px; }

/* 펜 애니메이션 */
.floating-pen {
  animation: writing-float 2s ease-in-out infinite;
  transform-origin: center;
}

@keyframes writing-float {
  0% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-5px) rotate(-5deg); }
  100% { transform: translateY(0px) rotate(0deg); }
}

.empty-state p {
  color: var(--text-muted);
  font-size: 1.05rem;
  line-height: 1.6;
  margin: 0;
  font-weight: 500;
}
</style>

<style>
/* scoped가 없는 style 태그는 전역 적용됩니다.
  다크모드([data-theme="dark"])에서 특정 요소의 색상을 강제로 덮어씁니다.
*/

/* 다크모드 버튼 */
[data-theme="dark"] .btn-create {
  background-color: #14428b !important;
  color: #e8eaed !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
}

/* 다크모드 뱃지 */
[data-theme="dark"] .badge {
  color: #6baaf7 !important;
}

/* 다크모드 링크 호버 */
[data-theme="dark"] .col-title a:hover {
  color: #6baaf7 !important;
}

/* 다크모드: 빈 상태 아이콘 SVG 내부 색상 변경 */
[data-theme="dark"] .empty-icon-box svg rect[fill="white"] {
  fill: #1F2937; /* 문서 배경 어둡게 */
  stroke: #374151; /* 테두리 어둡게 */
}
[data-theme="dark"] .empty-icon-box svg path[stroke="#F3F4F6"] {
  stroke: #374151; /* 문서 내부 줄 어둡게 */
}
</style>