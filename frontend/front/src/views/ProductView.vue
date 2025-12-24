<template>
  <div class="page-container">
    <div class="content-wrapper">
      
      <div class="header-section">
        <div class="title-area">
          <span class="sub-badge">금융 상품</span>
          <h1>💰 예적금 비교</h1>
        </div>

        <div class="controls">
          <div class="tab-group">
            <button 
              :class="{ active: activeTab === 'deposit' }" 
              @click="activeTab = 'deposit'"
            >
              정기예금
            </button>
            <button 
              :class="{ active: activeTab === 'saving' }" 
              @click="activeTab = 'saving'"
            >
              정기적금
            </button>
          </div>

          <div class="select-wrapper">
            <select v-model="selectedBank" class="bank-select">
              <option value="all">전체 은행 보기</option>
              <option v-for="bank in bankList" :key="bank" :value="bank">
                {{ bank }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div v-if="filteredProducts.length === 0" class="no-data">
        <div class="spinner"></div>
        <p>데이터를 불러오는 중입니다...</p>
      </div>

      <div v-else class="table-card">
        <div class="table-scroll">
          <table>
            <thead>
              <tr>
                <th width="15%">금융회사</th>
                <th width="25%">상품명</th>
                <th width="10%">6개월</th>
                <th width="10%">12개월</th>
                <th width="10%">24개월</th>
                <th width="10%">36개월</th>
                <th width="20%">가입방법</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="product in filteredProducts" 
                :key="product.id" 
                @click="goDetail(product)"
              >
                <td class="bank-name">
                  <div class="bank-logo-placeholder">{{ product.kor_co_nm[0] }}</div>
                  {{ product.kor_co_nm }}
                </td>
                <td class="product-name">{{ product.fin_prdt_nm }}</td>
                <td class="rate">{{ getInterestRate(product, 6) }}</td>
                <td class="rate main-rate">{{ getInterestRate(product, 12) }}</td>
                <td class="rate">{{ getInterestRate(product, 24) }}</td>
                <td class="rate">{{ getInterestRate(product, 36) }}</td>
                <td class="join-way">
                  <span class="tag">{{ product.join_way?.split(',')[0] }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance'
import { onMounted, ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const store = useFinanceStore()
const router = useRouter()

const selectedBank = ref('all')
const activeTab = ref('deposit')

onMounted(() => {
  store.getProducts()
  store.getSavingProducts()
})

const currentProductList = computed(() => {
  return activeTab.value === 'deposit' ? store.products : store.savingProducts
})

const bankList = computed(() => {
  const banks = currentProductList.value.map(p => p.kor_co_nm)
  return [...new Set(banks)]
})

const filteredProducts = computed(() => {
  let targetList = currentProductList.value
  
  if (selectedBank.value !== 'all') {
    targetList = targetList.filter(p => p.kor_co_nm === selectedBank.value)
  }
  return targetList
})

watch(activeTab, () => {
  selectedBank.value = 'all'
})

const getInterestRate = (product, term) => {
  const option = product.options?.find(opt => opt.save_trm === term)
  return option ? `${option.intr_rate}%` : '-'
}

const goDetail = (product) => {
  router.push({
    name: 'product-detail', 
    params: { id: product.fin_prdt_cd } 
  })
}
</script>

<style scoped>
/* 페이지 전체 배경 및 레이아웃 */
.page-container {
  background-color: #f2f4f6;
  min-height: 100vh;
  padding: 40px 20px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* 1. 헤더 섹션 */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.sub-badge {
  display: inline-block;
  color: #3182f6;
  font-weight: 700;
  margin-bottom: 8px;
  font-size: 14px;
}

.title-area h1 {
  font-size: 32px;
  font-weight: 800;
  color: #191f28;
  margin: 0;
}

.controls {
  display: flex;
  gap: 16px;
  align-items: center;
}

/* 탭 버튼 스타일 (토글 형태) */
.tab-group {
  background-color: #e8f3ff;
  padding: 4px;
  border-radius: 12px;
  display: flex;
}

.tab-group button {
  padding: 10px 24px;
  font-size: 15px;
  border: none;
  background: transparent;
  color: #7090b0;
  cursor: pointer;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.tab-group button.active {
  background-color: #3182f6;
  color: white;
  box-shadow: 0 2px 8px rgba(49, 130, 246, 0.3);
}

.tab-group button:hover:not(.active) {
  color: #3182f6;
}

/* 셀렉트 박스 */
.select-wrapper {
  position: relative;
}

.bank-select {
  padding: 12px 16px;
  font-size: 15px;
  border: 1px solid #d1d6db;
  border-radius: 12px;
  background-color: white;
  color: #333d4b;
  min-width: 180px;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

.bank-select:focus {
  border-color: #3182f6;
}

/* 2. 테이블 카드 스타일 */
.table-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  overflow: hidden; /* 모서리 둥글게 유지 */
  border: 1px solid rgba(0,0,0,0.03);
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

th {
  background-color: #f9fafb;
  color: #4e5968;
  font-weight: 600;
  padding: 18px;
  font-size: 14px;
  border-bottom: 1px solid #e5e8eb;
  white-space: nowrap;
}

td {
  padding: 20px 15px;
  border-bottom: 1px solid #f2f4f6;
  color: #4e5968;
  font-size: 15px;
  vertical-align: middle;
}

/* 행 호버 효과 */
tr {
  cursor: pointer;
  transition: background-color 0.2s;
}

tr:hover {
  background-color: #eff6ff; /* 연한 파란색 */
}

/* 테이블 내부 요소 스타일 */
.bank-name {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-weight: 700;
  color: #191f28;
}

.bank-logo-placeholder {
  width: 32px;
  height: 32px;
  background-color: #f2f4f6;
  color: #8b95a1;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.product-name {
  text-align: left;
  font-weight: 500;
  color: #333d4b;
}

.rate {
  font-variant-numeric: tabular-nums; /* 숫자 간격 일정하게 */
}

.main-rate {
  color: #3182f6;
  font-weight: 800;
  font-size: 16px;
}

.tag {
  background-color: #f2f4f6;
  color: #6b7684;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

/* 로딩/데이터 없음 */
.no-data {
  text-align: center;
  padding: 80px;
  color: #8b95a1;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f2f4f6;
  border-top-color: #3182f6;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .header-section {
    flex-direction: column;
    align-items: flex-start;
  }
  .controls {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }
  .tab-group, .select-wrapper {
    width: 100%;
  }
  .tab-group button {
    flex: 1;
  }
  .bank-select {
    width: 100%;
  }
  .product-name {
    text-align: center;
  }
  .bank-name {
    flex-direction: column;
  }
}
</style>