<template>
  <div class="detail-container" v-if="product">
    <div class="header-section">
      <span class="bank-badge">{{ product.kor_co_nm }}</span>
      <h1 class="product-title">{{ product.fin_prdt_nm }}</h1>
    </div>

    <div class="info-card">
      <div class="info-row">
        <span class="label">가입 대상</span>
        <span class="value">{{ product.join_member || '제한 없음' }}</span>
      </div>
      <div class="info-row">
        <span class="label">가입 방법</span>
        <span class="value">{{ product.join_way || '영업점, 스마트폰' }}</span>
      </div>
      <div class="info-row">
        <span class="label">우대 조건</span>
        <span class="value description">{{ product.spcl_cnd || '없음' }}</span>
      </div>
      
      <div class="rate-section">
        <h3 class="rate-title">💰 기간별 금리 (연 %)</h3>
        <table class="rate-table">
          <thead>
            <tr>
              <th>계약 기간</th>
              <th>기본 금리</th>
              <th>최고 금리</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="opt in product.options" :key="opt.id">
              <td>{{ opt.save_trm }}개월</td>
              <td>{{ opt.intr_rate }}%</td>
              <td class="highlight">{{ opt.intr_rate2 }}%</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="info-row" style="border-top: 1px solid #f3f4f6; padding-top: 20px;">
        <span class="label">상품 설명</span>
        <span class="value description">{{ product.etc_note || '상세 설명이 없습니다.' }}</span>
      </div>
    </div>

    <div class="action-area">
      <button 
        v-if="store.isJoined(product.fin_prdt_cd)" 
        @click="store.cancelProduct(product.fin_prdt_cd)" 
        class="btn btn-danger"
      >
        💔 가입 취소
      </button>

      <button 
        v-else 
        @click="store.joinProduct(product)" 
        class="btn btn-primary"
      >
        💳 가입하기
      </button>

      <a 
        v-if="bankUrl"
        :href="bankUrl" 
        target="_blank" 
        class="btn btn-bank"
      >
        🏦 {{ product.kor_co_nm }} 공식 사이트
      </a>
      
      <button @click="router.back()" class="btn btn-secondary">뒤로가기</button>
    </div>
  </div>

  <div v-else class="loading-container">
    <div class="spinner"></div>
    <p>상품 정보를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'

const route = useRoute()
const router = useRouter()
const store = useFinanceStore()
const product = ref(null)

// 은행 URL 매핑
const mainBankUrls = {
  '국민은행': 'https://www.kbstar.com',
  '신한은행': 'https://www.shinhan.com',
  '우리은행': 'https://www.wooribank.com',
  '하나은행': 'https://www.kebhana.com',
  '농협은행': 'https://www.nhbank.com',
  '중소기업은행': 'https://www.ibk.co.kr',
  '한국스탠다드차타드은행': 'https://www.standardchartered.co.kr',
  '한국산업은행': 'https://www.kdb.co.kr',
  '수협은행': 'https://www.suhyup-bank.com',
  '대구은행': 'https://www.dgb.co.kr',
  '부산은행': 'https://www.busanbank.co.kr',
  '광주은행': 'https://www.kjbank.com',
  '제주은행': 'https://www.e-jejubank.com',
  '전북은행': 'https://www.jbbank.co.kr',
  '경남은행': 'https://www.knbank.co.kr',
  '카카오뱅크': 'https://www.kakaobank.com',
  '토스뱅크': 'https://www.tossbank.com',
  '케이뱅크': 'https://www.kbanknow.com',
}

const bankUrl = computed(() => {
  if (!product.value) return null
  const bankName = product.value.kor_co_nm
  
  if (mainBankUrls[bankName]) return mainBankUrls[bankName]
  for (const key in mainBankUrls) {
    if (bankName.includes(key)) return mainBankUrls[key]
  }
  if (bankName.includes('저축은행')) return 'https://www.fsb.or.kr' 
  return null
})

onMounted(async () => {
  const productId = route.params.id
  let found = findProduct(productId)

  if (found) {
    product.value = found
  } else {
    // 새로고침 대응
    if (store.products.length === 0) await store.getProducts()
    if (store.savingProducts.length === 0) await store.getSavingProducts()
    
    found = findProduct(productId)
    if (found) product.value = found
    else {
      alert('상품 정보를 찾을 수 없습니다.')
      router.back()
    }
  }
})

const findProduct = (id) => {
  return store.products.find(p => p.fin_prdt_cd === id) || store.savingProducts.find(p => p.fin_prdt_cd === id)
}
</script>

<style scoped>
.detail-container { max-width: 800px; margin: 60px auto; padding: 0 20px; }
.header-section { text-align: center; margin-bottom: 40px; }

.bank-badge { 
  background-color: var(--bg-badge); 
  color: #4a86e8; 
  font-weight: 700; 
  padding: 8px 16px; 
  border-radius: 20px; 
}

.product-title { 
  margin-top: 15px; 
  font-size: 2.2rem; 
  font-weight: 800; 
  color: var(--text-primary); 
  letter-spacing: -1px; 
}

.info-card { 
  background: var(--bg-card); 
  border-radius: 20px; 
  padding: 40px; 
  box-shadow: 0 10px 30px var(--shadow-color); 
  border: 1px solid var(--border-color); 
  margin-bottom: 40px; 
}

.info-row { display: flex; padding: 18px 0; border-bottom: 1px solid var(--border-color); }
.label { width: 120px; font-weight: 600; color: var(--text-muted); flex-shrink: 0; }
.value { color: var(--text-primary); font-weight: 500; line-height: 1.6; flex: 1; }
.description { white-space: pre-line; word-break: keep-all; color: var(--text-secondary); }

/* ▼ 금리 테이블 스타일 */
.rate-section { 
  margin: 20px 0; 
  background-color: var(--bg-body); 
  padding: 20px; 
  border-radius: 12px; 
}
.rate-title { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 15px; }

.rate-table { 
  width: 100%; 
  border-collapse: collapse; 
  background: var(--bg-card); 
  border-radius: 8px; 
  overflow: hidden; 
}
.rate-table th { background-color: var(--bg-hover); color: var(--text-secondary); padding: 12px; }
.rate-table td { padding: 12px; border-bottom: 1px solid var(--border-color); color: var(--text-primary); }

.highlight { color: #ff6b6b; font-weight: 800; }

/* 버튼들을 감싸는 영역 */
.action-area {
  display: flex;
  justify-content: center; /* ✨ 버튼들을 가로 중앙으로 정렬 */
  align-items: center;     /* 세로 중앙 정렬 */
  gap: 16px;               /* 버튼 사이 간격 */
  margin-top: 40px;        /* 카드와의 간격 */
  width: 100%;             /* 전체 너비 사용 */
}

/* 버튼 공통 스타일 */
.btn { 
  padding: 14px 28px; 
  border-radius: 12px; 
  font-weight: 700; 
  font-size: 1rem; 
  cursor: pointer; 
  transition: all 0.2s; 
  text-decoration: none; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center;
  border: none;
  min-width: 140px; /* ✨ 버튼들이 너무 작아지지 않게 최소 너비 지정 */
}


/* 뒤로가기 버튼 다크모드 대응 */
.btn-secondary { 
  background-color: var(--bg-card);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}
.btn-secondary:hover {
  background-color: var(--bg-hover);
}

.btn-bank { background-color: #14428b; color: white; }
:global([data-theme="light"]) .btn-bank { background-color: #3b82f6; }

/* 로딩 스타일 */
.spinner { border: 4px solid var(--border-color); border-top: 4px solid #42b983; }
/* 반응형: 화면이 작아지면 버튼을 세로로 쌓고 싶을 때 (선택 사항) */
@media (max-width: 600px) {
  .action-area {
    flex-direction: column; /* 모바일에서는 세로로 */
    gap: 10px;
  }
  .btn {
    width: 100%; /* 모바일에서는 버튼이 꽉 차게 */
  }
}
</style>