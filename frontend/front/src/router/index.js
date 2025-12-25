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

import YoutubeSearchView from '@/views/YoutubeSearchView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue' 
import ChatView from '@/views/ChatView.vue'

import SubscriptionListView from '@/views/SubscriptionListView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import DepositView from '@/views/DepositView.vue'

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
    {
      path: '/chatbot',
      name: 'chatbot',
      component: ChatView
    },
  // ▼▼▼ [유튜브 관련 라우터] ▼▼▼
    {
      path: '/search',
      name: 'youtube-search',
      component: YoutubeSearchView
    },
    {
      path: '/video/:id',
      name: 'video-detail',
      component: VideoDetailView
    },
    {
      path: '/joined-products',
      name: 'subscription-list',
      component: SubscriptionListView
    },
    {
      path: '/deposit',
      name: 'deposit',
      component: DepositView
    },
    {
      path: '/products/:id', // id 파라미터 필요
      name: 'product-detail',
      component: ProductDetailView
    },
    {
      path: '/chat',
      name: 'chatbot',
      component: ChatView
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    // 사용자가 뒤로가기/앞으로가기를 눌렀을 때는 이전 스크롤 위치를 유지
    if (savedPosition) {
      return savedPosition
    } else {
      // 새 페이지로 이동할 때는 항상 맨 위로 (x:0, y:0)
      return { top: 0 }
    }
  }
})

export default router