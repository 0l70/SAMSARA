<template>
  <div class="board-container">
    <h1>📌 자유 게시판</h1>
    
    <div class="actions">
      <RouterLink :to="{ name: 'article-create' }" class="btn-create">
        글쓰기
      </RouterLink>
    </div>

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
        <tr v-for="(article, index) in store.articles" :key="article.id">
          
          <td>{{ index + 1 }}</td>

          <td class="title-col">
            <RouterLink :to="{ name: 'article-detail', params: { id: article.id }}">
              {{ article.title }}
            </RouterLink>
          </td>
          <td>{{ article.username }}</td>
          <td>{{ article.created_at?.substring(0, 10) }}</td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="store.articles.length === 0" style="text-align: center; margin-top: 50px; color: #999;">
      작성된 게시글이 없습니다.
    </div>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { RouterLink } from 'vue-router'

const store = useArticleStore()

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.board-container { max-width: 800px; margin: 40px auto; padding: 20px; }
.actions { text-align: right; margin-bottom: 20px; }
.btn-create { 
  background-color: #42b983; color: white; padding: 10px 20px; 
  text-decoration: none; border-radius: 5px; font-weight: bold; 
}
.article-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.article-table th { background-color: #f8f9fa; padding: 12px; border-bottom: 2px solid #ddd; }
.article-table td { padding: 12px; border-bottom: 1px solid #eee; text-align: center; }
.title-col { text-align: left !important; padding-left: 20px; }
.title-col a { text-decoration: none; color: #333; font-weight: bold; }
.title-col a:hover { color: #42b983; }
</style>