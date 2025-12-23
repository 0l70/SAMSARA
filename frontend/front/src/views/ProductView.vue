<template>
  <div class="container">
    <div class="header-section">
      <h1>💰 금융 상품 비교</h1>
      
      <div class="control-box">
        <select v-model="selectedBank" class="bank-select">
          <option value="all">전체 은행 보기</option>
          <option v-for="bank in bankList" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>
    </div>

    <div class="tabs">
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

    <hr>

    <div v-if="filteredProducts.length === 0" class="no-data">
      <p>로딩 중이거나 데이터가 없습니다.</p>
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th width="15%">금융회사</th>
            <th width="30%">상품명</th>
            <th width="10%">6개월</th>
            <th width="10%">12개월</th>
            <th width="10%">24개월</th>
            <th width="10%">36개월</th>
            <th width="15%">가입방법</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="product in filteredProducts" 
            :key="product.id" 
            @click="goDetail(product)"
          >
            <td class="bank-name">{{ product.kor_co_nm }}</td>
            <td class="product-name">{{ product.fin_prdt_nm }}</td>
            <td class="rate">{{ getInterestRate(product, 6) }}</td>
            <td class="rate highlight">{{ getInterestRate(product, 12) }}</td>
            <td class="rate">{{ getInterestRate(product, 24) }}</td>
            <td class="rate">{{ getInterestRate(product, 36) }}</td>
            <td class="join-way">{{ product.join_way }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance'
import { onMounted, ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router' // ★ 라우터 import

const store = useFinanceStore()
const router = useRouter() // ★ 라우터 사용 설정

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
  // 옵션이 없을 경우 에러 방지 (?.)
  const option = product.options?.find(opt => opt.save_trm === term)
  return option ? `${option.intr_rate}%` : '-'
}

// ▼ 핵심 수정: 상세 페이지 이동 함수
const goDetail = (product) => {
  router.push({
    name: 'product-detail', // 라우터에 등록된 이름 (index.js 확인 필요)
    params: { id: product.fin_prdt_cd } // 상품 코드 전달
  })
}
</script>

<style scoped>
.container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
.header-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.bank-select { padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ddd; }
.table-container { overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 10px; margin-top: 20px; }
table { width: 100%; border-collapse: collapse; background-color: white; text-align: center; }
th { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #ddd; white-space: nowrap; font-weight: bold; }
td { padding: 15px; border-bottom: 1px solid #eee; color: #555; }

/* ▼ 핵심 수정: 마우스 올렸을 때 클릭 가능 표시 */
tr { cursor: pointer; transition: background-color 0.2s; } 
tr:hover { background-color: #e6f7ef; transform: scale(1.001); }

.bank-name { font-weight: bold; color: #2c3e50; }
.product-name { text-align: left; padding-left: 20px; }
.highlight { color: #e74c3c; font-weight: bold; }

/* 탭 스타일 */
.tabs { display: flex; gap: 10px; margin-bottom: 10px; }
.tabs button {
  padding: 12px 30px;
  font-size: 16px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  cursor: pointer;
  border-radius: 8px 8px 0 0;
  color: #777;
  transition: all 0.3s;
  border-bottom: none;
}
.tabs button.active {
  background-color: #42b983;
  color: white;
  font-weight: bold;
  border-color: #42b983;
}
.tabs button:hover:not(.active) { background-color: #eee; }

.no-data { text-align: center; padding: 50px; color: #888; }
</style>