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
            <th width="15%" v-if="activeTab === 'deposit'">가입방법</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.id">
            <td class="bank-name">{{ product.kor_co_nm }}</td>
            <td class="product-name">{{ product.fin_prdt_nm }}</td>
            <td class="rate">{{ getInterestRate(product, 6) }}</td>
            <td class="rate highlight">{{ getInterestRate(product, 12) }}</td>
            <td class="rate">{{ getInterestRate(product, 24) }}</td>
            <td class="rate">{{ getInterestRate(product, 36) }}</td>
            <td class="join-way" v-if="activeTab === 'deposit'">{{ product.join_way }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance'
import { onMounted, ref, computed, watch } from 'vue'

const store = useFinanceStore()
const selectedBank = ref('all')
const activeTab = ref('deposit') // 현재 탭 상태 ('deposit' or 'saving')

// 페이지 로드 시 둘 다 가져옴
onMounted(() => {
  store.getProducts()        // 예금
  store.getSavingProducts()  // 적금
})

// 현재 탭에 따라 보여줄 전체 리스트 결정
const currentProductList = computed(() => {
  return activeTab.value === 'deposit' ? store.products : store.savingProducts
})

// 은행 목록 필터용 (현재 보고 있는 리스트 기준)
const bankList = computed(() => {
  const banks = currentProductList.value.map(p => p.kor_co_nm)
  return [...new Set(banks)]
})

// 최종 필터링된 상품 리스트
const filteredProducts = computed(() => {
  let targetList = currentProductList.value
  
  if (selectedBank.value !== 'all') {
    targetList = targetList.filter(p => p.kor_co_nm === selectedBank.value)
  }
  return targetList
})

// 탭이 바뀌면 은행 선택 초기화
watch(activeTab, () => {
  selectedBank.value = 'all'
})

const getInterestRate = (product, term) => {
  const option = product.options.find(opt => opt.save_trm === term)
  return option ? `${option.intr_rate}%` : '-'
}
</script>

<style scoped>
/* 기존 스타일 유지 + 탭 스타일 추가 */
.container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
.header-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.bank-select { padding: 10px; font-size: 16px; border-radius: 5px; border: 1px solid #ddd; }
.table-container { overflow-x: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 10px; margin-top: 20px; }
table { width: 100%; border-collapse: collapse; background-color: white; text-align: center; }
th { background-color: #f8f9fa; padding: 15px; border-bottom: 2px solid #ddd; white-space: nowrap; font-weight: bold; }
td { padding: 15px; border-bottom: 1px solid #eee; color: #555; }
tr:hover { background-color: #f1f8f5; }
.bank-name { font-weight: bold; color: #2c3e50; }
.product-name { text-align: left; padding-left: 20px; }
.highlight { color: #e74c3c; font-weight: bold; }

/* ▼▼▼ 탭 버튼 스타일 */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.tabs button {
  padding: 12px 30px;
  font-size: 16px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  cursor: pointer;
  border-radius: 8px 8px 0 0; /* 위쪽만 둥글게 */
  color: #777;
  transition: all 0.3s;
  border-bottom: none;
}
.tabs button.active {
  background-color: #42b983; /* 활성화 색상 */
  color: white;
  font-weight: bold;
  border-color: #42b983;
}
.tabs button:hover:not(.active) {
  background-color: #eee;
}
</style>