<template>
  <div class="list-container">
    <div class="page-header">
      <h1>📂 내 가입 상품 리스트</h1>
      <p>관심 있게 본 금융 상품을 한곳에서 관리하세요.</p>
    </div>

    <div v-if="store.joinedProducts.length > 0" class="product-grid">
      <div 
        v-for="product in store.joinedProducts" 
        :key="product.fin_prdt_cd" 
        class="product-card"
        @click="goDetail(product.fin_prdt_cd)"
      >
        <div class="card-top">
          <span class="bank-name">{{ product.kor_co_nm }}</span>
        </div>
        <h3 class="card-title">{{ product.fin_prdt_nm }}</h3>
        <div class="card-bottom">
          <button class="detail-btn">상세보기 & 해지</button>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="icon">📭</div>
      <p>아직 가입한 상품이 없습니다.</p>
      <button @click="$router.push({ name: 'products' })" class="go-products-btn">
        상품 둘러보러 가기
      </button>
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
.list-container { max-width: 1200px; margin: 0 auto; padding: 50px 20px; }
.page-header { text-align: center; margin-bottom: 50px; }
.page-header h1 { font-size: 2.2rem; font-weight: 800; color: #2c3e50; margin-bottom: 10px; }
.page-header p { color: #666; font-size: 1.1rem; }

/* 카드 그리드 */
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; }

/* 카드 디자인 */
.product-card {
  background: white; border-radius: 16px; padding: 25px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05); cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s; border: 1px solid #eee;
  display: flex; flex-direction: column; justify-content: space-between; min-height: 180px;
}
.product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: #42b983; }

.card-top { margin-bottom: 15px; }
.bank-name { font-size: 0.9rem; font-weight: 700; color: #42b983; background: #e6f7ef; padding: 4px 10px; border-radius: 12px; }
.card-title { font-size: 1.3rem; font-weight: 700; color: #333; margin: 0; line-height: 1.4; }
.card-bottom { margin-top: 20px; text-align: right; }
.detail-btn { background: none; border: none; color: #888; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
.product-card:hover .detail-btn { color: #42b983; text-decoration: underline; }

/* 빈 상태 디자인 */
.empty-state { text-align: center; padding: 80px 0; background: #f8f9fa; border-radius: 20px; margin-top: 20px; }
.icon { font-size: 4rem; margin-bottom: 20px; }
.empty-state p { font-size: 1.2rem; color: #555; margin-bottom: 30px; }
.go-products-btn { background-color: #42b983; color: white; border: none; padding: 12px 25px; border-radius: 30px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: 0.3s; }
.go-products-btn:hover { background-color: #3aa876; }
</style>