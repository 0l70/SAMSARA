// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductView from '../views/ProductView.vue'
import SignUpView from '../views/SignUpView.vue'
import LogInView from '../views/LogInView.vue'
import ExchangeView from '../views/ExchangeView.vue'
import ArticleView from '../views/ArticleView.vue'
import ArticleCreateView from '../views/ArticleCreateView.vue'
import ArticleDetailView from '../views/ArticleDetailView.vue'
// ▼▼▼ [추가] 1. 은행 찾기 뷰 불러오기
import BankView from '../views/BankView.vue'
import MyPageView from '@/views/MyPageView.vue'
import GoldView from '../views/GoldView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'

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
    // ▼▼▼ [추가] 2. 은행 찾기 라우터 등록
    {
      path: '/bank',
      name: 'BankView', // 여기를 대문자로 바꾸면 App.vue를 안 고쳐도 됩니다.
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
      path: '/articles/:id/edit',
      name: 'article-update',
      component: ArticleUpdateView // 혹은 CreateView를 재사용한다면 ArticleCreateView
    },
    {
      path: '/articles/:id/edit',
      name: 'article-update',
      component: ArticleUpdateView
    },
  ]
})

export default router