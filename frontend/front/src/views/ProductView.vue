<template>
  <div class="page-container">
    <div class="content-wrapper">
      
      <div class="header-section">
        <div class="title-area">
          <span class="sub-badge">금융 상품</span>
          <h1>예적금 비교</h1>
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
  background-color: var(--bg-body);
  min-height: 100vh;
  padding: 40px 20px;
  transition: background-color 0.3s ease;
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
.controls {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-direction: row; /* 반드시 row(가로)여야 합니다 */
}
.sub-badge {
  display: inline-block;
  color: #4a86e8; /* 톤다운된 블루 */
  font-weight: 700;
  margin-bottom: 8px;
  font-size: 14px;
}

.title-area h1 {
  font-size: 32px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

/* 탭 버튼 스타일 */
.tab-group {
  background-color: var(--bg-badge);
  padding: 4px;
  border-radius: 12px;
  display: flex;
}

.tab-group button {
  padding: 10px 24px;
  font-size: 15px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.tab-group button.active {
  background-color: #4a86e8;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* 다크모드 전용 액티브 색상 */
:global([data-theme="dark"]) .tab-group button.active {
  background-color: #14428b;
}

/* 셀렉트 박스 */
.bank-select {
  padding: 12px 16px;
  font-size: 15px;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background-color: var(--bg-card);
  color: var(--text-primary);
  min-width: 180px;
  cursor: pointer;
  outline: none;
  transition: border-color 0.2s;
}

/* 2. 테이블 카드 스타일 */
.table-card {
  background: var(--bg-card);
  border-radius: 20px;
  box-shadow: 0 4px 20px var(--shadow-color);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

th {
  background-color: var(--bg-body);
  color: var(--text-secondary);
  font-weight: 600;
  padding: 18px;
  border-bottom: 1px solid var(--border-color);
}

td {
  padding: 20px 15px;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
}

tr:hover {
  background-color: var(--bg-hover);
}

.bank-name {
  font-weight: 700;
  color: var(--text-primary);
}

.product-name {
  color: var(--text-primary);
}

.main-rate {
  color: #4a86e8;
  font-weight: 800;
}

.tag {
  background-color: var(--bg-body);
  color: var(--text-muted);
}

/* 로딩 애니메이션 */
.spinner {
  border: 4px solid var(--border-color);
  border-top-color: #4a86e8;
}
</style>