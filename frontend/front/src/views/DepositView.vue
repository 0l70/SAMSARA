<template>
  <div class="container">
    <h1 class="page-title">💰 정기예금 검색</h1>
    
    <div class="table-container">
      <table class="product-table">
        <thead>
          <tr>
            <th>금융회사</th>
            <th>상품명</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>24개월</th>
            <th>가입방법</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="product in store.products" 
            :key="product.fin_prdt_cd"
            @click="goDetail(product.fin_prdt_cd)"
          >
            <td class="bank-name">{{ product.kor_co_nm }}</td>
            
            <td class="product-name">{{ product.fin_prdt_nm }}</td>
            
            <td class="rate">{{ product.rate_6 || '-' }}%</td>
            <td class="rate highlight">{{ product.rate_12 || '-' }}%</td> <td class="rate">{{ product.rate_24 || '-' }}%</td>
            
            <td class="join-way">{{ product.join_way }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'

const store = useFinanceStore()
const router = useRouter()

onMounted(() => {
  store.getProducts() // 데이터 불러오기
})

// ★ 상세 페이지 이동 함수
const goDetail = (id) => {
  // 라우터로 이동하면서 id를 전달합니다.
  router.push({ 
    name: 'product-detail', 
    params: { id: id } 
  })
}
</script>

<style scoped>
.container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
.page-title { font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #333; }

/* 테이블 스타일 */
.table-container {
  overflow-x: auto; /* 화면 작을 때 스크롤 */
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  border-radius: 10px;
  background: white;
}

.product-table {
  width: 100%;
  border-collapse: collapse; /* 테두리 겹침 방지 */
  text-align: center;
  font-size: 14px;
}

/* 헤더 스타일 */
.product-table thead tr {
  background-color: #f8f9fa;
  border-bottom: 2px solid #ececec;
  color: #555;
  font-weight: 700;
}
.product-table th { padding: 15px; }

/* 바디(내용) 스타일 */
.product-table tbody tr {
  border-bottom: 1px solid #eee;
  transition: all 0.2s; /* 부드러운 효과 */
  cursor: pointer; /* ★ 마우스 올리면 손가락 모양 (중요!) */
}

/* ★ 마우스 올렸을 때 효과 (Hover) */
.product-table tbody tr:hover {
  background-color: #f0fdf4; /* 연한 초록색 배경 */
  transform: scale(1.002); /* 아주 살짝 커짐 */
}

.product-table td { padding: 15px; vertical-align: middle; color: #444; }

/* 특정 컬럼 스타일 */
.bank-name { font-weight: 600; color: #666; }
.product-name { font-weight: bold; color: #333; text-align: left; padding-left: 20px; }
.rate { color: #666; }
.rate.highlight { color: #d32f2f; font-weight: bold; } /* 12개월 빨간색 강조 */
.join-way { font-size: 13px; color: #888; }
</style>