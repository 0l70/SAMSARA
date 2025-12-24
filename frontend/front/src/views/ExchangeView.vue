<template>
  <div class="page-container">
    
    <div class="header-section">
      <span class="badge-title">실시간 정보</span>
      <h1 class="page-title">💱 환율 계산기</h1>
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
            <b>⥮</b>
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
          <span class="info-icon"><b>※</b></span>
          적용 환율: 1 {{ selectedCurrency.unit }} = {{ selectedCurrency.rate.toLocaleString() }} 원
          <br>
          <span style="font-size:0.8em; color:#9ca3af;">({{ selectedCurrency.date }} 기준)</span>
        </div>
      </div>

      <div class="chart-card" v-if="selectedCurrency">
        <div class="chart-header">
          <h2>📉 {{ selectedCurrency.unit }} 최근 동향</h2>
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
  /* ▼▼▼ [수정] 레이아웃 및 헤더 스타일 추가 ▼▼▼ */
.page-container {
  display: flex;
  flex-direction: column; /* 세로 정렬로 변경 */
  align-items: center;    /* 가로 중앙 정렬 */
  min-height: 80vh;
  background-color: #f5f7fa;
  padding: 60px 20px;     /* 상단 여백 확보 */
}

/* 제목 섹션 스타일 */
.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.badge-title {
  background-color: var(--bg-badge); /* 변수 사용 */
  color: #4a86e8; /* 다크모드 가독성 블루 */
  font-weight: 700;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  display: inline-block;
  margin-bottom: 12px;
}

.page-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--text-primary); /* ✨ 고정값 #111에서 변수로 변경 */
  letter-spacing: -1px;
  margin: 0 0 10px 0;
}

.page-subtitle {
  color: var(--text-secondary); /* ✨ 고정값 #666에서 변수로 변경 */
  font-size: 1.1rem;
  margin: 0;
}
/* =====================
  1. 전체 레이아웃 및 배경
===================== */
/* =====================
  1. 전체 레이아웃 및 배경 (수정됨)
===================== */
.page-container { 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  min-height: 80vh; 
  /* ✨ 고정값 #f5f7fa 대신 변수 사용 */
  background-color: var(--bg-body); 
  padding: 60px 20px; 
  transition: background-color 0.3s ease; /* 부드러운 전환 효과 */
}

/* 나머지 디자인 배치는 그대로 유지됩니다 */
.loading-msg {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-size: 1.2rem;
  color: var(--text-muted);
  font-weight: 600;
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

/* =====================
  2. 카드 공통 스타일
===================== */
.exchange-card, .chart-card {
  background: var(--bg-card); /* 카드 배경 변수 */
  width: 100%;
  max-width: 480px;
  padding: 40px 30px;
  border-radius: 24px;
  box-shadow: 0 10px 30px var(--shadow-color);
  border: 1px solid var(--border-color);
  text-align: center;
  transition: all 0.3s ease;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 30px;
}

/* =====================
  3. 환율 입력 박스 (가시성 강화)
===================== */
.currency-box {
  background-color: var(--bg-body); /* 카드 내부 입력창 배경 */
  border-radius: 16px;
  padding: 20px;
  transition: all 0.2s ease;
  border: 1px solid var(--border-color);
}

/* 포커스 효과 */
.currency-box.input-active:focus-within {
  border-color: #4a86e8;
  background-color: var(--bg-card);
  box-shadow: 0 0 0 4px rgba(74, 134, 232, 0.15);
}

.result-box {
  background-color: var(--bg-badge); /* 결과창은 약간 다른 톤 */
  border: 1px solid rgba(74, 134, 232, 0.1);
}

.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.box-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-muted);
}

.currency-select, .currency-unit {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 1rem;
}

.currency-select {
  padding: 4px 8px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background-color: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
  outline: none;
}

.input-area {
  display: flex;
  justify-content: flex-end;
}

.amount-input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 2.5rem;
  font-weight: 800;
  text-align: right;
  color: var(--text-primary);
  outline: none;
  padding: 0;
  letter-spacing: -1px;
}

.result-text {
  color: #4a86e8;
  text-shadow: 0 0 8px rgba(74, 134, 232, 0.2);
}

/* =====================
  4. 스왑 아이콘 & 정보
===================== */
.swap-icon-wrapper {
  position: relative;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.swap-icon {
  position: absolute;
  top: -18px;
  background: var(--bg-card);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  border: 3px solid var(--bg-body);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 10px var(--shadow-color);
}

.swap-icon:hover {
  transform: rotate(180deg) scale(1.1);
  color: #4a86e8;
  border-color: #4a86e8;
}

.rate-info {
  margin-top: 25px;
  font-size: 0.9rem;
  color: var(--text-muted);
}

/* =====================
  5. 차트 섹션
===================== */
.chart-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.chart-header h2 {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0;
}

.badge {
  background-color: var(--bg-badge);
  color: #4a86e8;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 6px 12px;
  border-radius: 20px;
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
  font-size: 0.95rem;
  line-height: 1.5;
}

.chart-desc strong {
  color: #4a86e8;
}

/* 크롬 number 화살표 제거 */
.amount-input::-webkit-outer-spin-button,
.amount-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>