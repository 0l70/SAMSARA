<template>
  <div class="board-container">
    <h1>✏️ 게시글 수정</h1>
    
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
            rows="10"
            required
          ></textarea>
        </div>

        <div class="btn-group">
          <button type="submit" class="btn-submit">수정 완료</button>
          <button type="button" @click="router.back()" class="btn-cancel">취소</button>
        </div>
      </form>
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

// 1. 페이지 로드 시 기존 데이터 불러오기
onMounted(() => {
  axios.get(`${API_URL}/api/v1/articles/${route.params.id}/`)
    .then((res) => {
      article.value = res.data
    })
    .catch((err) => {
      console.log(err)
      alert('데이터를 불러올 수 없습니다.')
      router.back()
    })
})

// 2. 수정 요청 보내기
const updateArticle = function () {
  const payload = {
    id: route.params.id,
    title: article.value.title,
    content: article.value.content
  }

  // 스토어 액션 호출 (없으면 axios.put 직접 사용)
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
/* 기존 스타일 유지하면서 깔끔하게 */
.board-container { max-width: 800px; margin: 40px auto; padding: 20px; }
.form-wrapper { background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border: 1px solid #eee; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-weight: bold; margin-bottom: 8px; color: #333; }
.form-group input, .form-group textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; transition: border 0.3s; }
.form-group input:focus, .form-group textarea:focus { border-color: #42b983; outline: none; }
.btn-group { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-submit { background-color: #42b983; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; transition: background 0.3s; }
.btn-submit:hover { background-color: #3aa876; }
.btn-cancel { background-color: #95a5a6; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; }
</style>