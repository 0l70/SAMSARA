<template>
  <div class="create-container">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div class="form-group">
        <label for="title">제목</label>
        <input 
          type="text" 
          id="title" 
          v-model.trim="title" 
          placeholder="제목을 입력해주세요"
        >
      </div>
      
      <div class="form-group">
        <label for="content">내용</label>
        <textarea 
          id="content" 
          v-model.trim="content" 
          placeholder="내용을 입력하세요"
        ></textarea>
      </div>
      
      <button type="submit" class="submit-btn">작성하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useRouter } from 'vue-router'

const store = useArticleStore()
const router = useRouter()

const title = ref('')
const content = ref('')

const createArticle = function () {
  // 1. 입력값 검사
  if (!title.value) {
    alert('제목을 입력해주세요!')
    return
  }
  if (!content.value) {
    alert('내용을 입력해주세요!')
    return
  }

  const payload = {
    title: title.value,
    content: content.value
  }

  // 2. 서버 전송
  store.createArticle(payload)
    .then((res) => {
      console.log('게시글 작성 성공')
      router.push({ name: 'articles' }) // 성공 시 목록 페이지로 이동
    })
    .catch((err) => {
      console.log(err)
      // 에러 메시지 상세 확인
      if (err.response && err.response.data) {
        alert('작성 실패: ' + JSON.stringify(err.response.data))
      } else {
        alert('서버 에러가 발생했습니다.')
      }
    })
}
</script>

<style scoped>
.create-container { max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
.form-group { margin-bottom: 20px; display: flex; flex-direction: column; }
label { font-weight: bold; margin-bottom: 5px; }
input, textarea { padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
textarea { height: 200px; resize: vertical; }
.submit-btn { width: 100%; padding: 12px; background-color: #42b983; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 1.1rem; font-weight: bold; }
.submit-btn:hover { background-color: #3aa876; }
</style>