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
        <h3 class="rate-title">
          <svg class="icon-svg title-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
          기간별 금리 (연 %)
        </h3>
        
        <div class="table-container">
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
      </div>

      <div class="info-row" style="border-top: 1px solid var(--border-color); padding-top: 20px;">
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
        <svg class="icon-svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        가입 취소
      </button>

      <button 
        v-else 
        @click="store.joinProduct(product)" 
        class="btn btn-primary"
      >
        <svg class="icon-svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        가입하기
      </button>

      <a 
        v-if="bankUrl"
        :href="bankUrl" 
        target="_blank" 
        class="btn btn-bank"
      >
        <svg class="icon-svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        {{ product.kor_co_nm }} 공식 사이트
      </a>
      
      <button @click="router.back()" class="btn btn-secondary">
        뒤로가기
      </button>
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
  '아이엠뱅크' : 'https://www.imbank.co.kr'
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
  font-size: 0.9rem;
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
  border-radius: 24px; 
  padding: 40px; 
  box-shadow: 0 10px 30px var(--shadow-color); 
  border: 1px solid var(--border-color); 
  margin-bottom: 40px; 
}

.info-row { display: flex; padding: 18px 0; border-bottom: 1px solid var(--border-color); }
.label { width: 120px; font-weight: 600; color: var(--text-muted); flex-shrink: 0; }
.value { color: var(--text-primary); font-weight: 500; line-height: 1.6; flex: 1; }
.description { white-space: pre-line; word-break: keep-all; color: var(--text-secondary); }

/* ▼▼▼ 금리 섹션 스타일 수정 (요청사항 반영) ▼▼▼ */
.rate-section { 
  margin: 25px 0; 
  background-color: var(--bg-body); /* 회색 박스 배경 */
  padding: 20px 24px 30px 24px;   /* 상단 패딩 축소 (24 -> 20) */
  border-radius: 16px; 
}

.rate-title { 
  font-size: 1.15rem; 
  font-weight: 700; 
  color: var(--text-primary); 
  margin: 0 0 16px 0; /* 상단 여백 제거, 하단 여백 조정 */
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 테이블을 감싸는 박스가 아닌, 테이블 자체에 그림자 부여 */
.rate-table { 
  width: 100%; 
  border-collapse: separate; 
  border-spacing: 0;
  background: var(--bg-card); /* 테이블 배경 흰색 */
  border-radius: 12px; 
  overflow: hidden; 
  
  /* ✨ 핵심: 테이블에 입체적인 그림자 추가 */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); 
  border: 1px solid var(--border-color);
}

.rate-table th { 
  background-color: var(--bg-hover); 
  color: var(--text-secondary); 
  padding: 14px; 
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
  border-bottom: 1px solid var(--border-color);
}

.rate-table td { 
  padding: 14px; 
  border-bottom: 1px solid var(--border-color); 
  color: var(--text-primary); 
  text-align: center;
}
/* 마지막 줄은 보더 제거 */
.rate-table tr:last-child td { border-bottom: none; }
/* ▲▲▲ 금리 섹션 스타일 수정 끝 ▲▲▲ */

.highlight { color: #ff6b6b; font-weight: 800; }

/* 아이콘 공통 스타일 */
.icon-svg { width: 20px; height: 20px; stroke-width: 2px; }
.title-icon { color: #4a86e8; width: 24px; height: 24px; }

/* 버튼 영역 스타일 */
.action-area {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 40px;
  width: 100%;
}

.btn { 
  padding: 14px 28px; 
  border-radius: 12px; 
  font-weight: 700; 
  font-size: 1rem; 
  cursor: pointer; 
  transition: all 0.2s ease; 
  text-decoration: none; 
  display: inline-flex; 
  align-items: center; 
  justify-content: center;
  border: none;
  min-width: 140px; 
  gap: 8px; 
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.btn:hover { transform: translateY(-2px); filter: brightness(0.95); }
.btn-primary { background-color: #3b82f6; color: white; }
.btn-danger { background-color: #ef4444; color: white; }
.btn-bank { background-color: #4b5563; color: white; }
.btn-secondary { background-color: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color); box-shadow: none; }

:global([data-theme="light"]) .btn-bank { background-color: #1f2937; }

.loading-container { text-align: center; margin-top: 100px; }
.spinner { 
  border: 4px solid var(--border-color); 
  border-top: 4px solid #3b82f6; 
  border-radius: 50%; 
  width: 40px; 
  height: 40px; 
  animation: spin 1s linear infinite; 
  margin: 0 auto 20px;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

@media (max-width: 600px) {
  .action-area { flex-direction: column; gap: 12px; }
  .btn { width: 100%; }
}
</style>