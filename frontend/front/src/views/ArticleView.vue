<template>
  <div class="board-container">
    <h1>자유 게시판</h1>
    
    <div class="actions">
      <a href="#" class="btn-create" @click.prevent="goCreateArticle">
        글쓰기
      </a>
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
import { useRouter } from 'vue-router'

// 1. [중요] useCounterStore가 아니라 useAuthStore를 가져와야 합니다!
import { useAuthStore } from '@/stores/auth' 

const store = useArticleStore()
const router = useRouter()

// 2. 로그인 정보가 들어있는 스토어 연결
const authStore = useAuthStore() 

const goCreateArticle = () => {
  // 디버깅용 로그 (F12 콘솔에서 확인 가능)
  console.log('현재 토큰:', authStore.token)

  // 3. 토큰이 있으면 로그인 된 것으로 간주
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
/* 스타일은 그대로 두셔도 됩니다 */
.board-container { max-width: 800px; margin: 40px auto; padding: 20px; }
.actions { text-align: right; margin-bottom: 20px; }
.btn-create { 
  background-color: #42b983; color: white; padding: 10px 20px; 
  text-decoration: none; border-radius: 5px; font-weight: bold; 
  cursor: pointer; /* 마우스 올렸을 때 손가락 모양 나오게 추가 */
}
.article-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
.article-table th { background-color: #f8f9fa; padding: 12px; border-bottom: 2px solid #ddd; }
.article-table td { padding: 12px; border-bottom: 1px solid #eee; text-align: center; }
.title-col { text-align: left !important; padding-left: 20px; }
.title-col a { text-decoration: none; color: #333; font-weight: bold; }
.title-col a:hover { color: #42b983; }
</style>