import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export const useArticleStore = defineStore('article', () => {
  // 1. State
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()

  // --------------------------------------------------
  // 2. Actions
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
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/`,
      data: payload,
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // 👇 [추가 1] 게시글 수정 (이 부분이 없어서 에러가 났던 겁니다!)
  const updateArticle = function (payload) {
    const authStore = useAuthStore()
    const { id, title, content } = payload
    
    return axios({
      method: 'put',
      url: `${API_URL}/api/v1/articles/${id}/`,
      data: { title, content },
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [기능 3] 게시글 삭제
  const deleteArticle = function (articleId) {
    const authStore = useAuthStore()
    return axios({
      method: 'delete',
      url: `${API_URL}/api/v1/articles/${articleId}/`,
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [기능 4] 댓글 작성
  const createComment = function (articleId, content) {
    const authStore = useAuthStore()
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/${articleId}/comments/`,
      data: { content },
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [기능: 댓글 수정]
  const updateComment = function (payload) {
    const authStore = useAuthStore()
    const { commentId, content } = payload

    return axios({
      method: 'put',
      // 👇 [수정] 주소 중간에 /articles/ 를 넣었습니다!
      // (이전: /api/v1/comments/...)
      url: `${API_URL}/api/v1/articles/comments/${commentId}/`, 
      data: { content },
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // [기능: 댓글 삭제]
  const deleteComment = function (articleId, commentId) {
    const authStore = useAuthStore()
    return axios({
      method: 'delete',
      // 👇 [수정] 여기도 똑같이 /articles/ 추가
      url: `${API_URL}/api/v1/articles/comments/${commentId}/`,
      headers: { Authorization: `Token ${authStore.token}` }
    })
  }

  // 3. Return (밖으로 내보내기)
  return { 
    articles, 
    API_URL, 
    getArticles, 
    createArticle, 
    updateArticle, // 👈 [중요] 여기 꼭 있어야 Vue 파일에서 사용 가능합니다!
    deleteArticle, 
    createComment, 
    updateComment, // 👈 [중요] 여기도 추가됨
    deleteComment 
  }
})