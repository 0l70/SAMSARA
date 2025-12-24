<template>
  <div class="page-container">
    <div class="content-wrapper">
      
      <div class="header-section">
        <div class="title-area">
          <span class="sub-badge">MY PORTFOLIO</span>
          <h1>내 가입 상품 리스트</h1>
        </div>
        <p class="desc">관심 있게 본 금융 상품을 한곳에서 관리하세요.</p>
      </div>

      <div v-if="store.joinedProducts.length > 0" class="product-grid">
        <div 
          v-for="product in store.joinedProducts" 
          :key="product.fin_prdt_cd" 
          class="product-card"
          @click="goDetail(product.fin_prdt_cd)"
        >
          <div class="card-top">
            <div class="bank-badge">
              <span class="bank-name">{{ product.kor_co_nm }}</span>
            </div>
          </div>
          
          <h3 class="card-title">{{ product.fin_prdt_nm }}</h3>
          
          <div class="card-divider"></div>
          
          <div class="card-bottom">
            <span class="status-text">가입중</span>
            <span class="detail-link">상세보기 & 해지</span>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">📂</div>
        <h2>아직 가입한 상품이 없어요</h2>
        <p>나에게 딱 맞는 예적금 상품을 찾아보세요!</p>
        <button @click="$router.push({ name: 'products' })" class="go-products-btn">
          금융 상품 보러가기
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance'
import { useRouter } from 'vue-router'

const store = useFinanceStore()
const router = useRouter()

const goDetail = (id) => {
  router.push({ name: 'product-detail', params: { id } })
}
</script>

<style scoped>
/* =====================
  1. 전체 레이아웃 (ProductView와 통일)
===================== */
.page-container {
  background-color: var(--bg-body); /* #f2f4f6 대신 변수 사용 */
  min-height: 100vh;
  padding: 40px 20px;
  transition: background-color 0.3s ease;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* =====================
  2. 헤더 스타일 (다크모드 대응)
===================== */
.header-section {
  text-align: left;
  margin-bottom: 40px;
}

.sub-badge {
  display: inline-block;
  color: #3182f6;
  font-weight: 700;
  font-size: 14px;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.title-area h1 {
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary); /* #191f28 대신 변수 사용 */
  margin: 0 0 10px 0;
}

.desc {
  color: var(--text-muted); /* #8b95a1 대신 변수 사용 */
  font-size: 16px;
  margin: 0;
}

/* =====================
  3. 그리드 및 카드 디자인
===================== */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.product-card {
  background: var(--bg-card); /* white 대신 변수 사용 */
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 2px 12px var(--shadow-color); /* 그림자 변수 사용 */
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border: 1px solid var(--border-color); /* 테두리 변수 사용 */
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px var(--shadow-color);
  border-color: rgba(49, 130, 246, 0.5); /* 호버 시 블루 강조 */
}

/* 카드 상단 (은행 정보) */
.bank-badge {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bank-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-secondary); /* #4e5968 대신 변수 사용 */
}

/* 상품명 */
.card-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-primary); /* #191f28 대신 변수 사용 */
  margin: 0 0 20px 0;
  line-height: 1.4;
  word-break: keep-all;
}

/* 구분선 */
.card-divider {
  height: 1px;
  background-color: var(--border-color); /* #f2f4f6 대신 변수 사용 */
  margin-bottom: 16px;
  margin-top: auto;
}

/* 카드 하단 */
.status-text {
  font-size: 13px;
  font-weight: 600;
  color: #3182f6;
  background-color: var(--bg-badge); /* 배경색 변수 사용 */
  padding: 4px 8px;
  border-radius: 6px;
}

.detail-link {
  font-size: 14px;
  color: var(--text-muted);
  font-weight: 500;
  transition: color 0.2s;
}

.product-card:hover .detail-link {
  color: #3182f6;
  font-weight: 700;
}

/* =====================
  4. 빈 상태 디자인 (Empty State)
===================== */
.empty-state {
  text-align: center;
  padding: 100px 20px;
  background: var(--bg-card);
  border-radius: 24px;
  box-shadow: 0 4px 20px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.empty-state h2 {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.empty-state p {
  font-size: 16px;
  color: var(--text-muted);
  margin-bottom: 40px;
}

.go-products-btn {
  background-color: #3182f6;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(49, 130, 246, 0.3);
}

.go-products-btn:hover {
  background-color: #1b64da;
  transform: translateY(-2px);
}
</style>