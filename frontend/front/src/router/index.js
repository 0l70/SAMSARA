import { createRouter, createWebHistory } from 'vue-router'

// 1. 기존 뷰 Import
import HomeView from '../views/HomeView.vue'
import ProductView from '../views/ProductView.vue'
import SignUpView from '../views/SignUpView.vue'
import LogInView from '../views/LogInView.vue'
import ExchangeView from '../views/ExchangeView.vue'
import ArticleView from '../views/ArticleView.vue'
import ArticleCreateView from '../views/ArticleCreateView.vue'
import ArticleDetailView from '../views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import BankView from '../views/BankView.vue'
import MyPageView from '@/views/MyPageView.vue'
import GoldView from '../views/GoldView.vue'
import TestView from '../views/TestView.vue'

// 2. [추가] 유튜브 관련 뷰 Import
import YoutubeSearchView from '@/views/YoutubeSearchView.vue'
// ⚠️ 중요: 아래 파일이 실제로 만들어져 있어야 에러가 안 납니다!
import VideoDetailView from '@/views/VideoDetailView.vue' 

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/products',
      name: 'products',
      component: ProductView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/exchange',
      name: 'exchange',
      component: ExchangeView
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticleView
    },
    {
      path: '/articles/create',
      name: 'article-create',
      component: ArticleCreateView
    },
    {
      path: '/articles/:id',
      name: 'article-detail',
      component: ArticleDetailView
    },
    {
      path: '/articles/:id/edit',
      name: 'article-update',
      component: ArticleUpdateView
    },
    {
      path: '/bank',
      name: 'BankView',
      component: BankView
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView
    },
    {
      path: '/gold',
      name: 'gold',
      component: GoldView
    },
    {
      path: '/test',
      name: 'test',
      component: TestView
    },
  ]
})

export default router