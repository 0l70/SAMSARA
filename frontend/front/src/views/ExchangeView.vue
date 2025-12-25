<template>
  <div class="page-container">
    
    <div class="header-section">
      <span class="badge-title">실시간 정보</span>
      <h1 class="page-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="header-icon"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        환율 계산기
      </h1>
      <p class="page-subtitle">주요 통화의 실시간 환율을 확인하고 계산해보세요.</p>
    </div>

    <div v-if="loading" class="loading-msg">
      <div class="spinner"></div>
      <p>환율 정보를 불러오는 중입니다...</p>
    </div>

    <div v-else class="dashboard-layout">

      <div class="exchange-card">
        <h2 class="card-title">계산하기</h2>

        <div class="currency-box input-active">
          <div class="box-header">
            <label class="box-label">
              {{ !isSwapped ? '외화 (보낼 금액)' : 'KRW (보낼 금액)' }}
            </label>
            
            <select v-if="!isSwapped" v-model="selectedCurrency" @change="calculateFromTop" class="currency-select">
              <option v-for="currency in currencies" :key="currency.unit" :value="currency">
                {{ currency.unit }} ({{ currency.name }})
              </option>
            </select>

            <span v-else class="currency-unit">KRW (대한민국 원)</span>
          </div>
          
          <div class="input-area">
            <input 
              type="number" 
              v-model.number="topAmount" 
              @input="calculateFromTop"
              placeholder="0"
              class="amount-input"
            >
          </div>
        </div>

        <div class="swap-icon-wrapper">
          <div class="swap-icon" @click="toggleSwap" title="위아래 바꾸기">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M7 20V4"/>
              <path d="M3 8l4-4 4 4"/>
              
              <path d="M17 4v16"/>
              <path d="M13 16l4 4 4-4"/>
            </svg>
          </div>
        </div>

        <div class="currency-box result-box input-active">
           <div class="box-header">
            <label class="box-label">
              {{ isSwapped ? '외화 (받을 금액)' : 'KRW (받을 금액)' }}
            </label>

            <span v-if="!isSwapped" class="currency-unit">KRW (대한민국 원)</span>

            <select v-else v-model="selectedCurrency" @change="calculateFromBottom" class="currency-select">
              <option v-for="currency in currencies" :key="currency.unit" :value="currency">
                {{ currency.unit }} ({{ currency.name }})
              </option>
            </select>
          </div>
          
          <div class="input-area">
            <input 
              type="number" 
              v-model.number="bottomAmount" 
              @input="calculateFromBottom"
              placeholder="0"
              class="amount-input result-text"
            >
          </div>
        </div>

        <div class="rate-info" v-if="selectedCurrency">
          <span class="info-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
          </span>
          적용 환율: 1 {{ selectedCurrency.unit }} = {{ selectedCurrency.rate.toLocaleString() }} 원
          <br>
          <span style="font-size:0.8em; color:#9ca3af; margin-left: 20px;">({{ selectedCurrency.date }} 기준)</span>
        </div>
      </div>

      <div class="chart-card" v-if="selectedCurrency">
        <div class="chart-header">
          <h2 class="chart-title-flex">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px; color:#4a86e8;"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            {{ selectedCurrency.unit }} 최근 동향
          </h2>
          <span class="badge">최근 7일</span>
        </div>
        <div class="chart-wrapper">
          <Line :data="chartData" :options="chartOptions" />
        </div>
        <p class="chart-desc">
          최근 7일간의 <strong>{{ selectedCurrency.name }}</strong> 환율 변동 추이입니다.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue' // computed 제거 (직접 계산하므로)
import axios from 'axios'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

// ---------------------------------------------------------
// 상태 변수
// ---------------------------------------------------------
const currencies = ref([])
const currencyHistory = ref({})
const selectedCurrency = ref(null)

// ★ [수정] 양방향 바인딩을 위해 상단/하단 값을 별도로 관리
const topAmount = ref(null)    // 위쪽 입력값
const bottomAmount = ref(null) // 아래쪽 입력값

const isSwapped = ref(false)
const loading = ref(true)

// ---------------------------------------------------------
// 1. API 데이터 가져오기
// ---------------------------------------------------------
const fetchRates = async () => {
  try {
    loading.value = true
    // ★ 실제 API 주소 확인 필요
    const response = await axios.get('http://127.0.0.1:8000/api/v1/exchange/exchange-rates/')
    const rawData = response.data

    const processedData = rawData.map(item => {
      let unit = item.unit
      let name = item.name
      let rate = item.rate

      if (unit.endsWith('(100)')) {
        unit = unit.replace('(100)', '')
        rate = rate / 100
        name = name.replace('(100)', '')
      }
      return { date: item.search_date, unit, name, rate }
    })

    const latestMap = new Map()
    const historyMap = {}

    processedData.forEach(item => {
      if (!historyMap[item.unit]) historyMap[item.unit] = []
      historyMap[item.unit].push(item)

      if (!latestMap.has(item.unit)) {
        latestMap.set(item.unit, item)
      } else {
        const existing = latestMap.get(item.unit)
        if (new Date(item.date) > new Date(existing.date)) {
          latestMap.set(item.unit, item)
        }
      }
    })

    currencyHistory.value = historyMap
    const targetUnits = ['USD', 'JPY', 'EUR', 'CNY']
    currencies.value = Array.from(latestMap.values())
      .filter(c => targetUnits.includes(c.unit))

    const usd = currencies.value.find(c => c.unit === 'USD')
    selectedCurrency.value = usd || currencies.value[0]

  } catch (error) {
    console.error('환율 로딩 실패:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRates()
})

// ---------------------------------------------------------
// 2. [핵심] 양방향 계산 로직
// ---------------------------------------------------------

// (A) 위쪽 입력 시 -> 아래쪽 계산
const calculateFromTop = () => {
  if (!selectedCurrency.value) return
  const rate = selectedCurrency.value.rate
  const amount = topAmount.value

  // 입력값이 없으면 둘 다 비움
  if (amount === '' || amount === null) {
    bottomAmount.value = null
    return
  }

  if (!isSwapped.value) {
    // Top: 외화 -> Bottom: KRW
    bottomAmount.value = Math.floor(amount * rate)
  } else {
    // Top: KRW -> Bottom: 외화
    bottomAmount.value = parseFloat((amount / rate).toFixed(2))
  }
}

// (B) 아래쪽 입력 시 -> 위쪽 계산
const calculateFromBottom = () => {
  if (!selectedCurrency.value) return
  const rate = selectedCurrency.value.rate
  const amount = bottomAmount.value

  if (amount === '' || amount === null) {
    topAmount.value = null
    return
  }

  if (!isSwapped.value) {
    // Bottom: KRW -> Top: 외화
    topAmount.value = parseFloat((amount / rate).toFixed(2))
  } else {
    // Bottom: 외화 -> Top: KRW
    topAmount.value = Math.floor(amount * rate)
  }
}

// (C) 스왑 토글 (값도 같이 뒤집어줌)
const toggleSwap = () => {
  isSwapped.value = !isSwapped.value

  // 값이 있을 때만 스왑 처리
  if (topAmount.value || bottomAmount.value) {
    // 위쪽 값과 아래쪽 값을 서로 교체 (UX 향상)
    const temp = topAmount.value
    topAmount.value = bottomAmount.value
    bottomAmount.value = temp
  }
}

// 통화 종류가 바뀌면 위쪽 기준으로 재계산
watch(selectedCurrency, () => {
  calculateFromTop()
  chartData.value = getChartData()
})

// ---------------------------------------------------------
// 3. 차트 관련 (기존 유지)
// ---------------------------------------------------------
const getChartData = () => {
  if (!selectedCurrency.value) return { labels: [], datasets: [] }
  const unit = selectedCurrency.value.unit
  const history = currencyHistory.value[unit] || []
  const sortedHistory = [...history].sort((a, b) => new Date(a.date) - new Date(b.date))

  const labels = sortedHistory.map(item => {
    if (!item.date) return ''
    const dateObj = new Date(item.date)
    return `${dateObj.getMonth() + 1}.${dateObj.getDate()}`
  })
  const dataPoints = sortedHistory.map(item => item.rate)
  const color = '#3b82f6'

  return {
    labels: labels,
    datasets: [{
      label: '매매기준율',
      backgroundColor: (ctx) => {
        const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 300)
        gradient.addColorStop(0, 'rgba(59, 130, 246, 0.2)')
        gradient.addColorStop(1, 'rgba(59, 130, 246, 0.0)')
        return gradient
      },
      borderColor: color,
      borderWidth: 3,
      data: dataPoints,
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: '#fff',
      pointBorderColor: color,
      pointBorderWidth: 2
    }]
  }
}

const chartData = ref({ labels: [], datasets: [] })
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { 
      grid: { display: false }, 
      ticks: { 
        // 텍스트 색상을 변수에 맞추거나 동적으로 설정
        color: '#8b95a1', 
        font: { size: 11 } 
      } 
    },
    y: { 
      // 다크 모드일 때 선 색상을 더 어둡게 처리
      grid: { 
        color: 'rgba(139, 149, 161, 0.1)' 
      }, 
      ticks: {
        color: '#8b95a1',
        font: { size: 11 }
      },
      suggestedMin: (ctx) => {
        if(!ctx.chart.data.datasets.length) return 0;
        const values = ctx.chart.data.datasets[0].data;
        return Math.min(...values) * 0.995;
      }
    }
  }
}
</script>

<style scoped>
/* =========================================
   0. 디자인 시스템 (색상 변수 정의)
   ========================================= */
:root {
  /* 라이트 모드 (기본) */
  --primary-color: #4a86e8;       /* 메인 블루 */
  --bg-body: #f5f7fa;             /* 전체 배경 */
  --bg-card: #ffffff;             /* 카드 배경 */
  --bg-input: #ffffff;            /* 입력창 배경 */
  --bg-badge: #e8f0fe;            /* 뱃지 배경 */
  --text-primary: #111827;        /* 진한 텍스트 */
  --text-secondary: #4b5563;      /* 중간 텍스트 */
  --text-muted: #9ca3af;          /* 연한 텍스트 */
  --border-color: #e5e7eb;        /* 테두리 색상 */
  --shadow-color: rgba(0, 0, 0, 0.05); /* 그림자 */
}

/* (참고) 다크 모드 필요시 아래 주석 해제 후 body 등에 적용 */
/*
@media (prefers-color-scheme: dark) {
  :root {
    --bg-body: #111827;
    --bg-card: #1f2937;
    --bg-input: #1f2937;
    --bg-badge: #374151;
    --text-primary: #f9fafb;
    --text-secondary: #d1d5db;
    --text-muted: #9ca3af;
    --border-color: #374151;
    --shadow-color: rgba(0, 0, 0, 0.3);
  }
}
*/

/* =========================================
   1. 전체 레이아웃
   ========================================= */
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 80vh;
  background-color: var(--bg-body);
  padding: 60px 20px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  transition: background-color 0.3s ease;
}

.dashboard-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
  width: 100%;
  max-width: 1000px;
  align-items: center;
}

@media (min-width: 900px) {
  .dashboard-layout {
    flex-direction: row;
    align-items: stretch;
  }
  .exchange-card, .chart-card {
    flex: 1;
    max-width: none;
  }
}

.loading-msg {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  gap: 20px;
  font-size: 1.1rem;
  color: var(--text-muted);
}

/* =========================================
   2. 헤더 섹션
   ========================================= */
.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.badge-title {
  background-color: var(--bg-badge);
  color: var(--primary-color);
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.85rem;
  display: inline-block;
  margin-bottom: 12px;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -1px;
  margin: 0 0 10px 0;
  
  /* 아이콘과 텍스트 가로 정렬 */
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.header-icon {
  color: var(--primary-color);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

/* =========================================
   3. 카드 공통 스타일
   ========================================= */
.exchange-card, .chart-card {
  background: var(--bg-card);
  width: 100%;
  max-width: 480px;
  padding: 40px 30px;
  border-radius: 24px;
  box-shadow: 0 10px 30px var(--shadow-color);
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 30px;
  text-align: center;
}

/* =========================================
   4. 환율 입력 박스
   ========================================= */
.currency-box {
  background-color: var(--bg-input);
  border-radius: 16px;
  padding: 20px;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
}

/* 입력창 포커스 효과 */
.currency-box.input-active:focus-within {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 4px rgba(74, 134, 232, 0.15);
}

/* 결과창 스타일 (배경색 약간 다름) */
.result-box {
  background-color: var(--bg-badge);
  border: 1px solid rgba(74, 134, 232, 0.1);
}

.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.box-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-secondary);
}

/* 셀렉트 박스 */
.currency-select {
  padding: 6px 10px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-card);
  color: var(--text-primary);
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  outline: none;
}
.currency-select:hover {
  border-color: var(--primary-color);
}

.currency-unit {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 0.95rem;
}

/* 숫자 입력 영역 */
.input-area {
  display: flex;
  justify-content: flex-end;
}

.amount-input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 2.4rem;
  font-weight: 800;
  text-align: right;
  color: var(--text-primary);
  outline: none;
  padding: 0;
  letter-spacing: -1px;
  font-family: 'Roboto', sans-serif; /* 숫자가 예쁜 폰트 권장 */
}

.amount-input::placeholder {
  color: #d1d5db;
}

.result-text {
  color: var(--primary-color);
}

/* 크롬 Number Input 화살표 제거 */
.amount-input::-webkit-outer-spin-button,
.amount-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* =========================================
   5. 스왑(교환) 버튼 [핵심]
   ========================================= */
.swap-icon-wrapper {
  position: relative;
  height: 24px; /* 버튼이 들어갈 공간 확보 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 5;
}

.swap-icon {
  position: absolute;
  top: -20px; /* 두 박스 사이에 걸치도록 위치 조정 */
  
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 4px solid var(--bg-body); /* 배경색과 동일한 테두리로 간격 효과 */
  
  display: flex;
  justify-content: center;
  align-items: center;
  
  color: var(--text-muted);
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* 호버 시 애니메이션 */
.swap-icon:hover {
  transform: rotate(180deg) scale(1.1);
  background-color: var(--primary-color);
  color: #ffffff;
  border-color: var(--primary-color); /* 테두리까지 색상 변경 */
  box-shadow: 0 8px 20px rgba(74, 134, 232, 0.4);
}

/* =========================================
   6. 환율 정보 텍스트
   ========================================= */
.rate-info {
  margin-top: 25px;
  font-size: 0.9rem;
  color: var(--text-secondary);
  background-color: rgba(243, 244, 246, 0.5); /* 아주 연한 회색 박스 */
  padding: 12px;
  border-radius: 12px;
  
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
  line-height: 1.5;
}

.info-icon {
  display: flex;
  align-items: center;
  color: var(--primary-color);
}

/* =========================================
   7. 차트 섹션
   ========================================= */
.chart-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.chart-title-flex {
  display: flex;
  align-items: center;
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

.badge {
  background-color: var(--bg-badge);
  color: var(--primary-color);
  font-weight: 700;
  font-size: 0.8rem;
  padding: 4px 10px;
  border-radius: 12px;
}

.chart-wrapper {
  position: relative;
  height: 300px;
  width: 100%;
}

.chart-desc {
  margin-top: 20px;
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.chart-desc strong {
  color: var(--primary-color);
  font-weight: 700;
}
</style>