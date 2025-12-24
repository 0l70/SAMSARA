<template>
  <div class="page-bg">
    <div class="create-container">
      <h1 class="page-title">게시글 작성</h1>
      <p class="sub-title">금융 생활에 대한 이야기를 자유롭게 남겨보세요.</p>
      
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

  store.createArticle(payload)
    .then((res) => {
      console.log('게시글 작성 성공')
      router.push({ name: 'articles' }) 
    })
    .catch((err) => {
      console.log(err)
      if (err.response && err.response.data) {
        alert('작성 실패: ' + JSON.stringify(err.response.data))
      } else {
        alert('서버 에러가 발생했습니다.')
      }
    })
}
</script>

<style scoped>
/* 배경 및 레이아웃 */
.page-bg { background-color: #f2f4f6; min-height: 100vh; padding: 40px 20px; }
.create-container { max-width: 700px; margin: 0 auto; background: white; padding: 40px; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }

/* 타이포그래피 */
.page-title { font-size: 24px; font-weight: 700; color: #191f28; margin-bottom: 8px; }
.sub-title { color: #8b95a1; font-size: 15px; margin-bottom: 30px; }

/* 폼 스타일 */
.form-group { margin-bottom: 24px; display: flex; flex-direction: column; }
label { font-weight: 600; margin-bottom: 8px; color: #333d4b; font-size: 15px; }

input, textarea { 
  width: 100%; 
  padding: 14px 16px; 
  border: 1px solid #e5e8eb; 
  border-radius: 12px; 
  font-size: 16px; 
  background-color: #f9fafb; 
  transition: all 0.2s;
  box-sizing: border-box;
}

input:focus, textarea:focus { 
  outline: none; 
  border-color: #3182f6; 
  background-color: white; 
  box-shadow: 0 0 0 2px rgba(49, 130, 246, 0.1);
}

textarea { height: 250px; resize: none; }

/* 버튼 */
.submit-btn { 
  width: 100%; 
  padding: 16px; 
  background-color: #3182f6; /* 토스 블루 */
  color: white; 
  border: none; 
  border-radius: 16px; 
  cursor: pointer; 
  font-size: 17px; 
  font-weight: 700; 
  transition: background-color 0.2s;
  margin-top: 10px;
}
.submit-btn:hover { background-color: #1b64da; }
</style>