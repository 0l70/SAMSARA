<template>
  <div class="page-bg">
    <div class="board-container">
      <h1 class="page-title">게시글 수정</h1>
      
      <div class="form-wrapper">
        <form @submit.prevent="updateArticle">
          <div class="form-group">
            <label for="title">제목</label>
            <input 
              type="text" 
              id="title" 
              v-model="article.title" 
              placeholder="제목을 입력하세요"
              required
            >
          </div>

          <div class="form-group">
            <label for="content">내용</label>
            <textarea 
              id="content" 
              v-model="article.content" 
              placeholder="내용을 입력하세요"
              required
            ></textarea>
          </div>

          <div class="btn-group">
            <button type="button" @click="router.back()" class="btn-cancel">취소</button>
            <button type="submit" class="btn-submit">수정 완료</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()
const authStore = useAuthStore()

const article = ref({
  title: '',
  content: ''
})

const API_URL = 'http://127.0.0.1:8000'

onMounted(() => {
  axios.get(`${API_URL}/api/v1/articles/${route.params.id}/`)
    .then((res) => { article.value = res.data })
    .catch((err) => {
      console.log(err)
      alert('데이터를 불러올 수 없습니다.')
      router.back()
    })
})

const updateArticle = function () {
  const payload = {
    id: route.params.id,
    title: article.value.title,
    content: article.value.content
  }

  store.updateArticle(payload) 
    .then(() => {
      alert('수정되었습니다.')
      router.push({ name: 'article-detail', params: { id: route.params.id } })
    })
    .catch((err) => {
      console.log(err)
      alert('수정 실패! (권한이 없거나 서버 오류)')
    })
}
</script>

<style scoped>
.page-bg { background-color: #f2f4f6; min-height: 100vh; padding: 40px 20px; }
.board-container { max-width: 800px; margin: 0 auto; }
.page-title { font-size: 24px; font-weight: 700; color: #191f28; margin-bottom: 20px; text-align: center; }

.form-wrapper { background: #fff; padding: 40px; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
.form-group { margin-bottom: 24px; }
.form-group label { display: block; font-weight: 600; margin-bottom: 8px; color: #333; font-size: 15px; }

input, textarea { 
  width: 100%; 
  padding: 14px; 
  border: 1px solid #e5e8eb; 
  border-radius: 12px; 
  background-color: #f9fafb; 
  font-size: 16px; 
  box-sizing: border-box; 
  transition: 0.2s; 
}
input:focus, textarea:focus { 
  border-color: #3182f6; 
  background: white; 
  outline: none; 
}
textarea { height: 300px; resize: none; }

.btn-group { display: flex; justify-content: flex-end; gap: 10px; margin-top: 30px; }
.btn-submit { background-color: #3182f6; color: white; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 600; cursor: pointer; transition: 0.2s; font-size: 15px; }
.btn-submit:hover { background-color: #1b64da; }
.btn-cancel { background-color: #f2f4f6; color: #333; border: none; padding: 12px 24px; border-radius: 12px; font-weight: 600; cursor: pointer; font-size: 15px; }
.btn-cancel:hover { background-color: #e5e8eb; }
</style>