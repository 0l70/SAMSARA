<template>
  <div v-if="article" class="detail-container">
    <h1>{{ article.title }}</h1>
    <div class="info-row">
      <span>작성자: <strong>{{ article.username }}</strong></span>
      <span> | </span>
      <span>{{ article.created_at?.substring(0,10) }}</span>
    </div>

    <hr>
    
    <div class="content">{{ article.content }}</div>
    
    <hr>

    <div class="comment-section">
      <h3>💬 댓글</h3>

      <div v-if="authStore.isLogin" class="comment-form">
        <input 
          type="text" 
          v-model="commentContent" 
          placeholder="댓글을 입력하세요..." 
          @keyup.enter="createComment"
        >
        <button @click="createComment" class="btn-comment">등록</button>
      </div>
      <div v-else class="login-plz">
        댓글을 작성하려면 로그인이 필요합니다.
      </div>

      <div class="comment-list">
        <div 
          v-for="comment in article.comment_set" 
          :key="comment.id" 
          class="comment-item"
        >
          <div class="comment-main">
            <span class="comment-writer">{{ comment.username }}</span>
            <span class="comment-text">{{ comment.content }}</span>
          </div>
          
          <button 
            v-if="authStore.username === comment.username"
            @click="deleteComment(comment.id)"
            class="btn-cmt-delete"
          >
            삭제
          </button>
        </div>

        <div v-if="!article.comment_set || article.comment_set.length === 0" class="no-comment">
          작성된 댓글이 없습니다.
        </div>
      </div>
    </div>
    <div class="btn-group">
      <RouterLink :to="{ name: 'articles' }" class="btn-back">목록으로</RouterLink>
      
      <button 
        v-if="authStore.username === article.username" 
        @click="deleteArticle" 
        class="btn-delete"
      >
        글 삭제하기
      </button>
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
const commentContent = ref('') // 댓글 입력 데이터
const API_URL = 'http://127.0.0.1:8000'

// 1. 게시글(+댓글) 불러오기 함수
const fetchArticle = () => {
  axios.get(`${API_URL}/api/v1/articles/${route.params.id}/`)
    .then(res => {
      console.log('게시글 데이터:', res.data) 
      article.value = res.data
    })
    .catch(err => {
      console.log(err)
      alert('게시글을 불러오는 중 에러가 발생했습니다.')
    })
}

onMounted(() => {
  fetchArticle()
})

// 2. 게시글 삭제 기능
const deleteArticle = function () {
  if (confirm('정말 이 게시글을 삭제하시겠습니까?')) {
    store.deleteArticle(article.value.id)
      .then(() => {
        window.alert('삭제되었습니다.')
        router.push({ name: 'articles' })
      })
      .catch((err) => window.alert('삭제 실패!'))
  }
}

// 3. 댓글 작성 기능 (디버깅 강화 버전)
const createComment = function () {
  // 입력값 검증
  if (!commentContent.value.trim()) {
    alert('내용을 입력해주세요.')
    return
  }
  
  // 로그인 검증 (화면엔 보이지만 토큰이 없을 수 있음)
  if (!authStore.token) {
    alert('로그인 정보가 만료되었습니다. 다시 로그인해주세요.')
    return
  }

  // 서버 요청
  store.createComment(article.value.id, commentContent.value)
    .then(() => {
      // 성공 시 처리
      alert('댓글이 등록되었습니다!')
      commentContent.value = '' // 입력창 비우기
      fetchArticle() // 댓글 목록 새로고침
    })
    .catch((err) => {
      console.log('댓글 작성 에러:', err)
      
      // 에러 원인별 알림
      if (err.response) {
        const status = err.response.status
        if (status === 401) {
          alert('인증 실패: 로그인이 필요합니다.')
        } else if (status === 400) {
          alert('입력 정보 오류: 내용을 확인해주세요. (혹은 백엔드 read_only_fields 확인)')
        } else if (status === 404) {
          alert('서버 주소 오류: 백엔드 URL을 확인해주세요.')
        } else {
          alert(`서버 에러 (${status}): 잠시 후 다시 시도해주세요.`)
        }
      } else {
        alert('서버와 연결할 수 없습니다.')
      }
    })
}

// 4. 댓글 삭제 기능
const deleteComment = function (commentId) {
  if (confirm('댓글을 삭제하시겠습니까?')) {
    store.deleteComment(article.value.id, commentId)
      .then(() => {
        fetchArticle() // 목록 갱신
      })
      .catch((err) => {
        console.log(err)
        alert('댓글 삭제 실패')
      })
  }
}
</script>

<style scoped>
.detail-container { max-width: 800px; margin: 50px auto; padding: 30px; border: 1px solid #ddd; border-radius: 10px; }
.info-row { color: #666; margin-bottom: 20px; }
.content { min-height: 200px; white-space: pre-wrap; line-height: 1.6; margin: 20px 0; font-size: 1.1rem; }
.btn-group { display: flex; justify-content: space-between; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px;}
.btn-back { text-decoration: none; color: #555; padding: 10px 20px; background-color: #f1f1f1; border-radius: 5px; }
.btn-delete { background-color: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-weight: bold; }

/* 댓글 스타일 */
.comment-section { margin-top: 30px; background-color: #f9f9f9; padding: 20px; border-radius: 8px; }
.comment-form { display: flex; gap: 10px; margin-bottom: 20px; }
.comment-form input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
.btn-comment { background-color: #42b983; color: white; border: none; padding: 0 20px; border-radius: 4px; cursor: pointer; font-weight: bold;}
.login-plz { color: #999; margin-bottom: 20px; font-size: 0.9rem; }

.comment-list { display: flex; flex-direction: column; gap: 10px; }
.comment-item { display: flex; justify-content: space-between; align-items: center; background: white; padding: 10px 15px; border-radius: 4px; border: 1px solid #eee; }
.comment-writer { font-weight: bold; margin-right: 10px; color: #333; font-size: 0.9rem; }
.comment-text { color: #555; }
.btn-cmt-delete { background: none; border: none; color: #ff6b6b; cursor: pointer; font-size: 0.8rem; }
.btn-cmt-delete:hover { text-decoration: underline; }
.no-comment { text-align: center; color: #aaa; padding: 10px; }
</style>