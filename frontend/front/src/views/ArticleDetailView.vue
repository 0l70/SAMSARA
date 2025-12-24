<template>
  <div class="page-container">
    <div v-if="article" class="detail-wrapper">
      
      <div class="article-card">
        <div class="article-header">
          <span class="badge">Community</span>
          <h1 class="title">{{ article.title }}</h1>
          
          <div class="meta-data">
            <div class="left-info">
              <span class="author">{{ article.username }}</span>
              <span class="dot">·</span>
              <span class="date">{{ article.created_at?.substring(0, 10) }}</span>
            </div>

            <div v-if="authStore.username === article.username" class="action-buttons">
              <button @click="goUpdateArticle" class="btn-text">수정</button>
              <span class="divider-vertical"></span>
              <button @click="deleteArticle" class="btn-text delete">삭제</button>
            </div>
          </div>
        </div>

        <div class="divider"></div>
        
        <div class="article-content">
          {{ article.content }}
        </div>
      </div>

      <div class="comment-section">
        <h3 class="comment-title">댓글 <span class="highlight">{{ article.comment_set?.length || 0 }}</span></h3>

        <div v-if="authStore.token" class="comment-form">
          <input 
            type="text" 
            v-model="commentContent" 
            placeholder="따뜻한 댓글을 남겨주세요 :)" 
            @keyup.enter="createComment"
            class="comment-input"
          >
          <button @click="createComment" class="btn-comment-submit">등록</button>
        </div>
        <div v-else class="login-plz">
          <p>💬 댓글을 작성하려면 <RouterLink :to="{ name: 'login' }">로그인</RouterLink>이 필요합니다.</p>
        </div>

        <div class="comment-list">
          <div 
            v-for="comment in article.comment_set" 
            :key="comment.id" 
            class="comment-item"
          >
            <div v-if="editingCommentId !== comment.id" class="comment-view">
              <div class="comment-avatar-area">
                <div class="avatar-circle">{{ comment.username.charAt(0) }}</div>
              </div>
              <div class="comment-body">
                <div class="comment-header">
                  <span class="comment-writer">{{ comment.username }}</span>
                  <div v-if="authStore.username === comment.username" class="comment-actions">
                    <button @click="startEditComment(comment)" class="btn-mini">수정</button>
                    <button @click="deleteComment(comment.id)" class="btn-mini delete">삭제</button>
                  </div>
                </div>
                <p class="comment-text">{{ comment.content }}</p>
              </div>
            </div>

            <div v-else class="comment-edit-box">
              <input 
                type="text" 
                v-model="editingContent" 
                @keyup.enter="updateComment(comment.id)"
                class="edit-input"
              >
              <div class="edit-btns">
                <button @click="cancelEditComment" class="btn-small-cancel">취소</button>
                <button @click="updateComment(comment.id)" class="btn-small-save">저장</button>
              </div>
            </div>
          </div>

          <div v-if="!article.comment_set || article.comment_set.length === 0" class="no-comment">
            <p>아직 댓글이 없습니다. 첫 댓글의 주인공이 되어보세요! 🥳</p>
          </div>
        </div>
      </div>

      <div class="bottom-area">
        <button @click="router.push({ name: 'articles' })" class="btn-list">
          목록으로 돌아가기
        </button>
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

const article = ref(null)
const commentContent = ref('')
const API_URL = 'http://127.0.0.1:8000'

const editingCommentId = ref(null)
const editingContent = ref('')

const fetchArticle = () => {
  axios.get(`${API_URL}/api/v1/articles/${route.params.id}/`)
    .then(res => { article.value = res.data })
    .catch(err => { console.log(err) })
}

onMounted(() => { fetchArticle() })

const goUpdateArticle = () => {
  router.push({ name: 'article-update', params: { id: article.value.id } })
}

const deleteArticle = () => {
  if (confirm('정말 이 게시글을 삭제하시겠습니까?')) {
    store.deleteArticle(article.value.id)
      .then(() => {
        router.push({ name: 'articles' })
      })
      .catch(err => alert('삭제 실패!'))
  }
}

const createComment = () => {
  if (!commentContent.value.trim()) return
  store.createComment(article.value.id, commentContent.value)
    .then(() => {
      commentContent.value = ''
      fetchArticle()
    })
    .catch(err => alert('댓글 등록 실패'))
}

const deleteComment = (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    store.deleteComment(article.value.id, commentId)
      .then(() => fetchArticle())
      .catch(err => alert('삭제 실패'))
  }
}

const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

const cancelEditComment = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

const updateComment = (commentId) => {
  const payload = { commentId: commentId, content: editingContent.value }
  store.updateComment(payload)
    .then(() => {
      editingCommentId.value = null
      fetchArticle()
    })
    .catch(err => { console.log(err); alert('댓글 수정 실패') })
}
</script>

<style scoped>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css");

.page-container {
  /* ✨ 배경색 변수 적용 */
  background-color: var(--bg-body);
  min-height: 100vh;
  padding: 60px 20px;
  font-family: 'Pretendard', sans-serif;
  display: flex;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.detail-wrapper {
  width: 100%;
  max-width: 800px;
}

/* 게시글 카드 디자인 */
.article-card {
  /* ✨ 카드 배경 변수 적용 */
  background: var(--bg-card);
  padding: 50px;
  border-radius: 24px;
  /* ✨ 그림자 변수 적용 */
  box-shadow: 0 10px 30px var(--shadow-color);
  margin-bottom: 30px;
  border: 1px solid var(--border-color); /* 테두리 추가 (다크모드 구분용) */
}

.badge {
  /* ✨ 뱃지 변수 적용 */
  background-color: var(--bg-badge);
  color: var(--primary-color);
  font-size: 0.8rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 12px;
  display: inline-block;
}

.title {
  font-size: 2.2rem;
  font-weight: 800;
  /* ✨ 제목 색상 변수 적용 */
  color: var(--text-primary);
  margin: 0 0 20px 0;
  line-height: 1.3;
  letter-spacing: -0.5px;
}

/* 메타 정보 */
.meta-data {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* ✨ 메타 텍스트 색상 변수 */
  color: var(--text-muted);
  font-size: 0.95rem;
}

.left-info { display: flex; align-items: center; font-weight: 500; }
.author { 
  /* ✨ 작성자 이름 색상 변수 */
  color: var(--text-primary); 
  font-weight: 600; 
}
.dot { margin: 0 8px; color: var(--border-color); }

.action-buttons { display: flex; align-items: center; }
.divider-vertical { width: 1px; height: 12px; background: var(--border-color); margin: 0 10px; }

.btn-text { 
  background: none; 
  border: none; 
  color: var(--text-muted); 
  cursor: pointer; 
  font-size: 0.9rem; 
  padding: 0; 
  transition: color 0.2s; 
}
.btn-text:hover { color: var(--text-primary); text-decoration: underline; }
.btn-text.delete:hover { color: #fa5252; }

.divider { height: 1px; background: var(--border-color); margin: 30px 0; }

.article-content {
  font-size: 1.1rem;
  line-height: 1.8;
  /* ✨ 본문 색상 변수 */
  color: var(--text-secondary);
  white-space: pre-wrap;
  min-height: 200px;
}

/* 댓글 섹션 */
.comment-section {
  background: var(--bg-card);
  padding: 40px;
  border-radius: 24px;
  box-shadow: 0 10px 30px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.comment-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-primary);
}
.highlight { color: var(--primary-color); margin-left: 4px; }

/* 댓글 입력창 */
.comment-form {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  /* ✨ 입력폼 배경: 다크모드에서 구분되도록 hover 색상 사용 */
  background: var(--bg-hover);
  padding: 10px;
  border-radius: 16px;
  border: 1px solid var(--border-color);
}

.comment-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 10px 15px;
  font-size: 1rem;
  outline: none;
  font-family: 'Pretendard', sans-serif;
  /* ✨ 입력 글자색 중요 */
  color: var(--text-primary);
}

.btn-comment-submit {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-comment-submit:hover { filter: brightness(0.9); }

.login-plz {
  text-align: center;
  padding: 20px;
  background: var(--bg-hover);
  border-radius: 16px;
  color: var(--text-muted);
  margin-bottom: 30px;
}
.login-plz a { color: var(--primary-color); font-weight: 700; text-decoration: none; }

/* 댓글 리스트 아이템 */
.comment-list { display: flex; flex-direction: column; gap: 20px; }
.comment-item { border-bottom: 1px solid var(--border-color); padding-bottom: 20px; }
.comment-item:last-child { border-bottom: none; padding-bottom: 0; }

.comment-view { display: flex; gap: 15px; }

.avatar-circle {
  width: 40px;
  height: 40px;
  /* ✨ 아바타 배경 변수 */
  background-color: var(--bg-hover);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.comment-body { flex: 1; }
.comment-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.comment-writer { font-weight: 700; color: var(--text-primary); font-size: 0.95rem; }
.comment-text { color: var(--text-secondary); font-size: 1rem; line-height: 1.5; margin: 0; }

.btn-mini { background: none; border: none; font-size: 0.8rem; color: var(--text-muted); cursor: pointer; margin-left: 8px; }
.btn-mini:hover { color: var(--text-primary); }
.btn-mini.delete:hover { color: #fa5252; }

/* 댓글 수정 모드 */
.comment-edit-box { padding: 10px; background: var(--bg-hover); border-radius: 12px; }
.edit-input { 
  width: 100%; 
  border: 1px solid var(--border-color); 
  padding: 10px; 
  border-radius: 8px; 
  margin-bottom: 10px; 
  box-sizing: border-box; 
  background: transparent;
  color: var(--text-primary);
}
.edit-btns { display: flex; justify-content: flex-end; gap: 8px; }
.btn-small-save { background: var(--primary-color); color: white; border: none; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.85rem; font-weight: 600; }
.btn-small-cancel { background: var(--bg-body); color: var(--text-secondary); border: 1px solid var(--border-color); padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.85rem; }

.no-comment { text-align: center; color: var(--text-muted); padding: 30px 0; }

/* 하단 버튼 */
.bottom-area { margin-top: 40px; text-align: center; }
.btn-list {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 12px 30px;
  border-radius: 50px;
  color: var(--text-secondary);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(0,0,0,0.03);
}
.btn-list:hover {
  background: var(--bg-hover);
  transform: translateY(-2px);
  color: var(--text-primary);
  box-shadow: 0 6px 12px var(--shadow-color);
}
</style>