<template>
  <div class="page-container">
    <div class="editor-card">
      
      <div class="editor-header">
        <div class="top-row">
          <span class="badge">Edit Mode</span>
          <button type="button" @click="router.back()" class="btn-close">✕ 닫기</button>
        </div>
        
        <input 
          type="text" 
          id="title" 
          v-model="article.title" 
          placeholder="제목을 입력하세요"
          required
          class="input-title"
        >
      </div>

      <div class="divider"></div>
      
      <form @submit.prevent="updateArticle" class="editor-body">
        <textarea 
          id="content" 
          v-model="article.content" 
          placeholder="내용을 수정해보세요..."
          required
          class="textarea-content"
        ></textarea>

        <div class="bottom-bar">
          <div class="btn-group">
            <button type="button" @click="router.back()" class="btn-cancel">취소</button>
            <button type="submit" class="btn-submit">수정 완료</button>
          </div>
        </div>
      </form>
      
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()

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
      router.push({ name: 'article-detail', params: { id: route.params.id } })
    })
    .catch((err) => {
      console.log(err)
      alert('수정 실패! (권한이 없거나 서버 오류)')
    })
}
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css");

.page-container {
  /* 배경색 변수 */
  background-color: var(--bg-body);
  height: 100%;
  min-height: auto;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  font-family: 'Pretendard', sans-serif;
}

.editor-card {
  width: 100%;
  max-width: 900px;
  /* 카드 배경 변수 */
  background-color: var(--bg-card);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 10px 40px var(--shadow-color);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;
}

.editor-header { margin-bottom: 20px; }

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.badge {
  background-color: var(--bg-badge); /* 뱃지 배경 변수 */
  color: #3182f6;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 20px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1rem;
  /* 아이콘 색상 변수 */
  color: var(--text-muted);
  cursor: pointer;
  font-weight: 600;
  transition: color 0.2s;
}
.btn-close:hover { color: var(--text-primary); }

.input-title {
  width: 100%;
  border: none;
  font-size: 2.2rem;
  font-weight: 800;
  /* 입력 텍스트 색상 변수 */
  color: var(--text-primary);
  outline: none;
  padding: 10px 0;
  background: transparent;
}
.input-title::placeholder { color: var(--text-muted); }

.divider {
  height: 1px;
  background-color: var(--border-color); /* 구분선 변수 */
  margin-bottom: 30px;
}

.editor-body {
  display: flex;
  flex-direction: column;
}

.textarea-content {
  width: 100%;
  min-height: 40vh;
  border: none;
  resize: vertical;
  font-size: 1.1rem;
  line-height: 1.8;
  /* 입력 텍스트 색상 변수 */
  color: var(--text-primary);
  outline: none;
  background: transparent;
  font-family: 'Pretendard', sans-serif;
  margin-bottom: 30px;
}
.textarea-content::placeholder { color: var(--text-muted); }

.bottom-bar {
  border-top: 1px solid var(--border-color);
  padding-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.btn-group { display: flex; gap: 12px; }

button {
  padding: 14px 28px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-cancel {
  background-color: var(--bg-body); /* 취소 버튼 배경 */
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}
.btn-cancel:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.btn-submit {
  background-color: #3182f6;
  color: white;
  box-shadow: 0 4px 12px rgba(49, 130, 246, 0.2);
}
.btn-submit:hover {
  background-color: #1b64da;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(49, 130, 246, 0.3);
}

@media (max-width: 600px) {
  .editor-card { padding: 30px 20px; }
  .input-title { font-size: 1.8rem; }
  .textarea-content { min-height: 30vh; font-size: 1rem; }
  .btn-group { width: 100%; }
  .btn-group button { flex: 1; }
}
</style>