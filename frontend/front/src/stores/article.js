import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // auth 스토어 경로 확인

export const useArticleStore = defineStore('article', () => {
  // 1. State (상태 변수)
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  // --------------------------------------------------
  // 2. Actions (기능 함수들)
  // --------------------------------------------------

  // [기능 1] 게시글 전체 조회
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`
    })
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // [기능 2] 게시글 작성
  const createArticle = function (payload) {
    const authStore = useAuthStore()
    
    // axios 요청을 return 해줘야 Vue 컴포넌트에서 .then() 처리가 가능합니다.
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/`,
      data: payload,
      headers: {
        Authorization: `Token ${authStore.token}` // ★ 중요: 토큰 필수
      }
    })
  }

  // [기능 3] 게시글 삭제
  const deleteArticle = function (articleId) {
    const authStore = useAuthStore()

    return axios({
      method: 'delete',
      url: `${API_URL}/api/v1/articles/${articleId}/`, // 뒤에 슬래시(/) 주의
      headers: {
        Authorization: `Token ${authStore.token}` // ★ 중요: 토큰 없으면 401 에러
      }
    })
  }

  // [기능 4] 댓글 작성
  const createComment = function (articleId, content) {
    const authStore = useAuthStore()

    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
      data: {
        content: content
      },
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
  }

  // [기능 5] 댓글 삭제
  // 주의: backend/urls.py의 주소와 일치해야 합니다.
  const deleteComment = function (articleId, commentId) {
    const authStore = useAuthStore()

    return axios({
      method: 'delete',
      // 백엔드 urls.py에 path('comments/<int:comment_pk>/', ...) 로 설정했으므로
      url: `${API_URL}/api/v1/articles/comments/${commentId}/`,
      headers: {
        Authorization: `Token ${authStore.token}`
      }
    })
  }

  // 3. Return (밖으로 내보내기)
  return { 
    articles, 
    API_URL, 
    getArticles, 
    createArticle, 
    deleteArticle, 
    createComment, 
    deleteComment 
  }
})