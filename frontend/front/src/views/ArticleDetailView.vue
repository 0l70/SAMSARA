<template>
  <div v-if="article" class="detail-container">
    <div class="article-header">
      <h1 class="title">{{ article.title }}</h1>
      <div class="meta-info">
        <span class="author">👤 {{ article.username }}</span>
        <span class="date">📅 {{ article.created_at?.substring(0, 10) }}</span>
      </div>
    </div>

    <hr class="divider">
    
    <div class="content">{{ article.content }}</div>
    
    <hr class="divider">

    <div class="comment-section">
      <h3>💬 댓글 ({{ article.comment_set?.length || 0 }})</h3>

      <div v-if="authStore.token" class="comment-form">
        <input 
          type="text" 
          v-model="commentContent" 
          placeholder="따뜻한 댓글을 남겨주세요..." 
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
            <button @click="updateComment(comment.id)" class="btn-small-save">저장</button>
            <button @click="cancelEditComment" class="btn-small-cancel">취소</button>
          </div>
        </div>

        <div v-if="!article.comment_set || article.comment_set.length === 0" class="no-comment">
          첫 번째 댓글의 주인공이 되어보세요!
        </div>
      </div>
    </div>

    <div class="btn-group">
      <RouterLink :to="{ name: 'articles' }" class="btn-back">목록으로</RouterLink>
      
      <div v-if="authStore.username === article.username" class="right-btns">
        <button @click="goUpdateArticle" class="btn-update">수정</button>
        <button @click="deleteArticle" class="btn-delete">삭제</button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth' // ✅ auth 스토어 사용 확인
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()
const authStore = useAuthStore()

const article = ref(null)
const commentContent = ref('') // 댓글 작성용
const API_URL = 'http://127.0.0.1:8000'

// 댓글 수정 상태 관리
const editingCommentId = ref(null) // 현재 수정 중인 댓글 ID
const editingContent = ref('') // 수정 중인 내용

// ArticleDetailView.vue의 fetchArticle 함수 수정

const fetchArticle = () => {
  axios.get(`${API_URL}/api/v1/articles/${route.params.id}/`)
    .then(res => {
      article.value = res.data
      
      // 👇 [여기 추가] 이 3줄을 추가하고 F12 콘솔을 확인해주세요!
      console.log('게시글 작성자:', article.value.username)
      console.log('현재 로그인한 사람:', authStore.username)
      console.log('두 값이 같은가?:', article.value.username === authStore.username)
    })
    .catch(err => {
      console.log(err)
    })
}

onMounted(() => {
  fetchArticle()
})

// === 게시글 관련 함수 ===

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

// === 댓글 관련 함수 ===

// 댓글 등록
const createComment = () => {
  if (!commentContent.value.trim()) return
  
  store.createComment(article.value.id, commentContent.value)
    .then(() => {
      commentContent.value = ''
      fetchArticle() // 댓글 목록 갱신
    })
    .catch(err => alert('댓글 등록 실패'))
}

// 댓글 삭제
const deleteComment = (commentId) => {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    store.deleteComment(article.value.id, commentId)
      .then(() => fetchArticle())
      .catch(err => alert('삭제 실패'))
  }
}

// 댓글 수정 모드 진입
const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editingContent.value = comment.content
}

// 댓글 수정 취소
const cancelEditComment = () => {
  editingCommentId.value = null
  editingContent.value = ''
}

// 댓글 수정 완료 (서버 전송)
const updateComment = (commentId) => {
  const payload = {
    commentId: commentId,
    content: editingContent.value
  }
  
  // 👇 여기가 핵심! 직접 axios를 안 쓰고 스토어에 일을 시킵니다.
  store.updateComment(payload)
    .then(() => {
      console.log('수정 성공!')
      editingCommentId.value = null
      fetchArticle() // 목록 갱신
    })
    .catch(err => {
      console.log(err)
      alert('댓글 수정 실패')
    })
}
</script>

<style scoped>
.detail-container { max-width: 800px; margin: 50px auto; padding: 40px; border: 1px solid #e1e1e1; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); background: #fff; }

.article-header { margin-bottom: 20px; }
.title { font-size: 2rem; color: #333; margin-bottom: 10px; }
.meta-info { color: #888; font-size: 0.95rem; display: flex; gap: 15px; }
.divider { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
.content { min-height: 200px; line-height: 1.7; font-size: 1.1rem; white-space: pre-wrap; color: #444; }

/* 댓글 스타일 */
.comment-section { background-color: #f8f9fa; padding: 25px; border-radius: 10px; margin-top: 30px; }
.comment-form { display: flex; gap: 10px; margin-bottom: 25px; }
.comment-form input { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 15px; }
.btn-comment-submit { background-color: #42b983; color: white; border: none; padding: 0 25px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.btn-comment-submit:hover { background-color: #3aa876; }

.comment-list { display: flex; flex-direction: column; gap: 15px; }
.comment-item { background: white; padding: 15px; border-radius: 8px; border: 1px solid #eee; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

/* 댓글 읽기 모드 */
.comment-view { display: flex; justify-content: space-between; align-items: center; }
.comment-main { display: flex; flex-direction: column; gap: 5px; }
.comment-writer { font-weight: bold; color: #333; font-size: 0.9rem; }
.comment-text { color: #555; font-size: 1rem; }
.btn-text { background: none; border: none; color: #999; font-size: 0.85rem; cursor: pointer; margin-left: 10px; }
.btn-text:hover { text-decoration: underline; color: #3498db; }
.btn-text.delete:hover { color: #e74c3c; }

/* 댓글 수정 모드 */
.comment-edit { display: flex; gap: 10px; align-items: center; width: 100%; }
.edit-input { flex: 1; padding: 8px; border: 1px solid #42b983; border-radius: 4px; }
.btn-small-save { background: #42b983; color: white; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; }
.btn-small-cancel { background: #95a5a6; color: white; border: none; padding: 5px 12px; border-radius: 4px; cursor: pointer; }

/* 하단 버튼 그룹 */
.btn-group { display: flex; justify-content: space-between; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; }
.btn-back { padding: 10px 20px; background: #f1f3f5; color: #495057; border-radius: 6px; text-decoration: none; font-weight: bold; transition: 0.3s; }
.btn-back:hover { background: #e9ecef; }
.right-btns { display: flex; gap: 10px; }
.btn-update { background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }
.btn-update:hover { background-color: #2980b9; }
.btn-delete { background-color: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }
.btn-delete:hover { background-color: #c0392b; }
.login-plz { color: #999; text-align: center; margin-bottom: 20px; }
.login-plz a { color: #42b983; text-decoration: none; font-weight: bold; }
</style>