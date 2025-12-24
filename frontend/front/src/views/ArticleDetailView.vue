<template>
  <div class="page-bg">
    <div v-if="article" class="detail-container">
      <div class="article-header">
        <span class="badge">자유게시판</span>
        <h1 class="title">{{ article.title }}</h1>
        <div class="meta-info">
          <span class="author">{{ article.username }}</span>
          <span class="dot">·</span>
          <span class="date">{{ article.created_at?.substring(0, 10) }}</span>
        </div>
      </div>

      <div class="divider"></div>
      
      <div class="content">{{ article.content }}</div>
      
      <div class="divider"></div>

      <div class="comment-section">
        <h3>댓글 <span class="highlight">{{ article.comment_set?.length || 0 }}</span></h3>

        <div v-if="authStore.token" class="comment-form">
          <input 
            type="text" 
            v-model="commentContent" 
            placeholder="따뜻한 댓글을 남겨주세요" 
            @keyup.enter="createComment"
          >
          <button @click="createComment" class="btn-comment-submit">등록</button>
        </div>
        <div v-else class="login-plz">
          댓글을 작성하려면 <RouterLink :to="{ name: 'login' }">로그인</RouterLink>이 필요합니다.
        </div>

        <div class="comment-list">
          <div 
            v-for="comment in article.comment_set" 
            :key="comment.id" 
            class="comment-item"
          >
            <div v-if="editingCommentId !== comment.id" class="comment-view">
              <div class="comment-main">
                <span class="comment-writer">{{ comment.username }}</span>
                <span class="comment-text">{{ comment.content }}</span>
              </div>
              
              <div v-if="authStore.username === comment.username" class="comment-actions">
                <button @click="startEditComment(comment)" class="btn-text">수정</button>
                <button @click="deleteComment(comment.id)" class="btn-text delete">삭제</button>
              </div>
            </div>

            <div v-else class="comment-edit">
              <input 
                type="text" 
                v-model="editingContent" 
                @keyup.enter="updateComment(comment.id)"
                class="edit-input"
              >
              <div class="edit-btns">
                <button @click="updateComment(comment.id)" class="btn-small-save">저장</button>
                <button @click="cancelEditComment" class="btn-small-cancel">취소</button>
              </div>
            </div>
          </div>

          <div v-if="!article.comment_set || article.comment_set.length === 0" class="no-comment">
            아직 댓글이 없습니다. 첫 댓글을 남겨보세요! 💬
          </div>
        </div>
      </div>

      <div class="btn-group">
        <button @click="router.push({ name: 'articles' })" class="btn-back">
          ← 목록으로
        </button>
        
        <div v-if="authStore.username === article.username" class="right-btns">
          <button @click="goUpdateArticle" class="btn-secondary">수정</button>
          <button @click="deleteArticle" class="btn-danger">삭제</button>
        </div>
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
    .then(res => {
      article.value = res.data
      console.log('게시글 작성자:', article.value.username)
      console.log('현재 로그인한 사람:', authStore.username)
      console.log('두 값이 같은가?:', article.value.username === authStore.username)
    })
    .catch(err => { console.log(err) })
}

onMounted(() => { fetchArticle() })

const goUpdateArticle = () => {
  router.push({ name: 'article-update', params: { id: article.value.id } })
}

const deleteArticle = () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    store.deleteArticle(article.value.id)
      .then(() => {
        alert('게시글이 삭제되었습니다.')
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
      console.log('수정 성공!')
      editingCommentId.value = null
      fetchArticle()
    })
    .catch(err => { console.log(err); alert('댓글 수정 실패') })
}
</script>

<style scoped>
.page-bg { background-color: #f2f4f6; min-height: 100vh; padding: 40px 20px; }
.detail-container { max-width: 800px; margin: 0 auto; padding: 50px; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); background: #fff; }

/* 헤더 */
.badge { display: inline-block; padding: 6px 12px; background: #e8f3ff; color: #3182f6; border-radius: 8px; font-size: 13px; font-weight: 700; margin-bottom: 12px; }
.title { font-size: 28px; color: #191f28; margin-bottom: 12px; font-weight: 700; line-height: 1.3; }
.meta-info { color: #8b95a1; font-size: 15px; display: flex; align-items: center; }
.dot { margin: 0 8px; }

.divider { height: 1px; background: #f2f4f6; margin: 30px 0; }
.content { min-height: 200px; line-height: 1.7; font-size: 17px; white-space: pre-wrap; color: #333d4b; }

/* 댓글 섹션 */
.comment-section { margin-top: 40px; }
.comment-section h3 { font-size: 20px; color: #191f28; margin-bottom: 20px; font-weight: 700; }
.highlight { color: #3182f6; }

/* 댓글 입력 */
.comment-form { display: flex; gap: 10px; margin-bottom: 30px; }
.comment-form input { flex: 1; padding: 14px; border: 1px solid #e5e8eb; border-radius: 12px; font-size: 15px; background: #f9fafb; transition: 0.2s; }
.comment-form input:focus { outline: none; background: white; border-color: #3182f6; }
.btn-comment-submit { background-color: #3182f6; color: white; border: none; padding: 0 24px; border-radius: 12px; font-weight: 600; cursor: pointer; transition: 0.2s; }
.btn-comment-submit:hover { background-color: #1b64da; }

/* 댓글 리스트 */
.comment-list { display: flex; flex-direction: column; gap: 0; }
.comment-item { padding: 20px 0; border-bottom: 1px solid #f2f4f6; }
.comment-item:last-child { border-bottom: none; }

.comment-view { display: flex; justify-content: space-between; align-items: flex-start; }
.comment-main { display: flex; flex-direction: column; gap: 6px; }
.comment-writer { font-weight: 700; color: #4e5968; font-size: 14px; }
.comment-text { color: #191f28; font-size: 16px; line-height: 1.5; }

.btn-text { background: none; border: none; color: #8b95a1; font-size: 13px; cursor: pointer; margin-left: 8px; padding: 0; }
.btn-text:hover { text-decoration: underline; color: #333; }
.btn-text.delete:hover { color: #e11d48; }

/* 댓글 수정 모드 */
.comment-edit { width: 100%; }
.edit-input { width: 100%; padding: 10px; border: 1px solid #3182f6; border-radius: 8px; margin-bottom: 8px; box-sizing: border-box; }
.edit-btns { display: flex; gap: 8px; }
.btn-small-save { background: #3182f6; color: white; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; }
.btn-small-cancel { background: #f2f4f6; color: #333; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; }

.no-comment { text-align: center; color: #8b95a1; padding: 30px 0; font-size: 15px; }
.login-plz { color: #8b95a1; text-align: center; margin-bottom: 20px; }
.login-plz a { color: #3182f6; text-decoration: none; font-weight: 700; }

/* 하단 버튼 그룹 */
.btn-group { display: flex; justify-content: space-between; margin-top: 50px; align-items: center; }
.btn-back { background: none; border: none; color: #8b95a1; font-size: 16px; font-weight: 600; cursor: pointer; padding: 10px 0; }
.btn-back:hover { color: #333; }

.right-btns { display: flex; gap: 10px; }
.btn-secondary { background-color: #f2f4f6; color: #333; border: none; padding: 12px 20px; border-radius: 12px; cursor: pointer; font-weight: 600; }
.btn-secondary:hover { background-color: #e5e8eb; }
.btn-danger { background-color: #fff1f1; color: #e11d48; border: none; padding: 12px 20px; border-radius: 12px; cursor: pointer; font-weight: 600; }
.btn-danger:hover { background-color: #ffe4e4; }
</style>