<template>
  <div class="page-bg">
    <div class="board-container">
      <div class="header-group">
        <h1>자유 게시판</h1>
        <a href="#" class="btn-create" @click.prevent="goCreateArticle">
          글쓰기
        </a>
      </div>

      <div class="table-card">
        <table class="article-table">
          <thead>
            <tr>
              <th width="10%">번호</th>
              <th width="50%">제목</th>
              <th width="20%">작성자</th>
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
        
        <div v-if="store.articles.length === 0" class="empty-state">
          작성된 게시글이 없습니다.
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' 

const store = useArticleStore()
const router = useRouter()
const authStore = useAuthStore() 

const goCreateArticle = () => {
  console.log('현재 토큰:', authStore.token)
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
.page-bg { background-color: #f2f4f6; min-height: 100vh; padding: 40px 20px; }
.board-container { max-width: 900px; margin: 0 auto; }

/* 헤더 & 글쓰기 버튼 */
.header-group { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.header-group h1 { font-size: 26px; font-weight: 700; color: #191f28; margin: 0; }
.btn-create { 
  background-color: #3182f6; color: white; padding: 12px 20px; 
  text-decoration: none; border-radius: 12px; font-weight: 600; 
  cursor: pointer; transition: background-color 0.2s; font-size: 15px;
}
.btn-create:hover { background-color: #1b64da; }

/* 테이블 카드 디자인 */
.table-card { background: white; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); overflow: hidden; }

.article-table { width: 100%; border-collapse: collapse; }
.article-table th { 
  background-color: #f9fafb; 
  padding: 16px; 
  text-align: center; 
  color: #8b95a1; 
  font-weight: 600; 
  font-size: 14px;
  border-bottom: 1px solid #e5e8eb;
}
.article-table td { padding: 18px 16px; border-bottom: 1px solid #f2f4f6; text-align: center; color: #4e5968; font-size: 15px; }

.data-row:hover { background-color: #f8fbff; } /* 마우스 오버 시 연한 파랑 */
.data-row:last-child td { border-bottom: none; }

.col-id { color: #8b95a1; }
.col-title { text-align: left !important; padding-left: 20px; font-weight: 600; }
.col-title a { text-decoration: none; color: #333d4b; display: block; }
.col-title a:hover { color: #3182f6; }
.col-author { color: #4e5968; }
.col-date { color: #8b95a1; font-size: 14px; }

.empty-state { text-align: center; padding: 60px; color: #8b95a1; font-size: 15px; }
</style>