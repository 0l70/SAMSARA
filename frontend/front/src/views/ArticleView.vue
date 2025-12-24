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
          ✏️ 글쓰기
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
          <div class="empty-icon">📝</div>
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

.page-container {
  background-color: var(--bg-body);
  min-height: 100vh;
  padding: 60px 20px;
  font-family: 'Pretendard', sans-serif;
  transition: background-color 0.3s ease;
}

.board-wrapper { max-width: 1000px; margin: 0 auto; }

.header-group {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
}

.text-group { display: flex; flex-direction: column; }

.badge {
  background-color: var(--bg-badge);
  /* 라이트 모드 뱃지 색상 */
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

/* 라이트 모드(기본) 버튼 색상 */
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

.table-card {
  background: var(--bg-card);
  border-radius: 24px;
  box-shadow: 0 10px 30px var(--shadow-color);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: background-color 0.3s ease, border-color 0.3s ease;
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
.empty-state { text-align: center; padding: 80px 20px; color: var(--text-muted); }
.empty-icon { font-size: 3rem; margin-bottom: 15px; opacity: 0.5; }
</style>

<style>
/* scoped가 없으므로 Vue의 내부 ID와 상관없이 전역적으로 적용됩니다.
  !important를 붙여서 확실하게 색상을 덮어씁니다.
*/
[data-theme="dark"] .btn-create {
  background-color: #14428b !important; /* 차분한 네이비 */
  color: #e8eaed !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4) !important;
}

/* 뱃지 다크모드 색상 */
[data-theme="dark"] .badge {
  color: #6baaf7 !important;
}

/* 제목 링크 호버 시 다크모드 색상 */
[data-theme="dark"] .col-title a:hover {
  color: #6baaf7 !important;
}
</style>