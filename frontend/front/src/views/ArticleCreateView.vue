<template>
  <div class="page-container">
    <div class="editor-card">
      
      <div class="editor-header">
        <div class="top-row">
          <span class="badge">New Post</span>
          <button type="button" @click="goBack" class="btn-close">✕ 닫기</button>
        </div>
        
        <input 
          type="text" 
          id="title" 
          v-model.trim="title" 
          placeholder="제목을 입력하세요"
          class="input-title"
        >
      </div>

      <div class="divider"></div>
      
      <form @submit.prevent="createArticle" class="editor-body">
        <textarea 
          id="content" 
          v-model.trim="content" 
          placeholder="금융 생활에 대한 궁금증이나 꿀팁을 자유롭게 나눠보세요..."
          class="textarea-content"
        ></textarea>

        <div class="bottom-bar">
          <div class="btn-group">
            <button type="button" @click="goBack" class="btn-cancel">취소</button>
            <button type="submit" class="btn-submit">등록하기</button>
          </div>
        </div>
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

// 뒤로가기
const goBack = () => {
  router.back()
}

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
      // 성공 시 목록으로 이동
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
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css");

.page-container {
  background-color: var(--bg-body);
  height: 100%;
  min-height: auto;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  font-family: 'Pretendard', sans-serif;
  transition: background-color 0.3s ease;
}

.editor-card {
  width: 100%;
  max-width: 900px;
  background-color: var(--bg-card);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 10px 40px var(--shadow-color);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;
  border: 1px solid var(--border-color);
}

.editor-header { margin-bottom: 20px; }

.top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.badge {
  background-color: var(--bg-badge);
  /* 뱃지 글자색 톤다운 */
  color: #4a86e8;
  font-size: 0.85rem;
  font-weight: 700;
  padding: 6px 12px;
  border-radius: 20px;
}
:global([data-theme="dark"]) .badge { color: #6baaf7; }

.btn-close {
  background: none; border: none; font-size: 1rem;
  color: var(--text-muted); cursor: pointer; font-weight: 600;
  transition: color 0.2s;
}
.btn-close:hover { color: var(--text-primary); }

.input-title {
  width: 100%;
  border: none;
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  outline: none;
  padding: 10px 0;
  background: transparent;
}
.input-title::placeholder { color: var(--text-muted); }

.divider {
  height: 1px;
  background-color: var(--border-color);
  margin-bottom: 30px;
}

.editor-body { display: flex; flex-direction: column; }

.textarea-content {
  width: 100%;
  min-height: 40vh;
  border: none;
  resize: vertical;
  font-size: 1.1rem;
  line-height: 1.8;
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
  background-color: var(--bg-body);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}
.btn-cancel:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

/* ✨ [수정] 제출 버튼 (톤다운) */
.btn-submit {
  /* 차분한 파란색 */
  background-color: #4a86e8;
  color: white;
  box-shadow: 0 4px 12px rgba(74, 134, 232, 0.2);
}

/* ✨ [수정] 다크모드 제출 버튼 (더 차분하게) */
:global([data-theme="dark"]) .btn-submit {
  background-color: #395c96;
  color: #e8eaed;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.btn-submit:hover {
  filter: brightness(0.9);
  transform: translateY(-2px);
}

@media (max-width: 600px) {
  .editor-card { padding: 30px 20px; }
  .input-title { font-size: 1.8rem; }
  .textarea-content { min-height: 30vh; font-size: 1rem; }
  .btn-group { width: 100%; }
  .btn-group button { flex: 1; }
}
</style>