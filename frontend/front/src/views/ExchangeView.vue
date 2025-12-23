<template>
  <div class="page-container">
    
    <div v-if="loading" class="loading-msg">
      <p>⏳ 환율 정보를 불러오는 중입니다...</p>
    </div>

    <div v-else class="dashboard-layout">

      <div class="exchange-card">
        <h1 class="card-title">환율 계산기</h1>

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
    x: { grid: { display: false }, ticks: { color: '#6b7280', font: { size: 11 } } },
    y: { 
      grid: { color: '#f3f4f6' }, 
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
/* 기존 스타일 그대로 유지 */
.loading-msg { display: flex; justify-content: center; align-items: center; min-height: 80vh; font-size: 1.2rem; color: #6b7280; font-weight: 600; }
.page-container { display: flex; justify-content: center; align-items: center; min-height: 80vh; background-color: #f5f7fa; padding: 40px 20px; }
.exchange-card { background: white; width: 100%; max-width: 480px; padding: 40px 30px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); text-align: center; }
.card-title { font-size: 1.8rem; font-weight: 800; color: #1a1a1a; margin-bottom: 30px; }
.currency-box { background-color: #f3f4f6; border-radius: 16px; padding: 20px; transition: all 0.3s ease; border: 2px solid transparent; }
/* ★ 둘 다 입력 가능하므로 둘 다 focus 효과 적용 */
.currency-box.input-active:focus-within { border-color: #3b82f6; background-color: #fff; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15); }
.result-box { background-color: #eef2ff; }
.box-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.box-label { font-size: 0.95rem; font-weight: 600; color: #6b7280; }
.currency-select, .currency-unit { font-weight: 700; color: #374151; font-size: 1rem; }
.currency-select { padding: 4px 8px; border: 1px solid #d1d5db; border-radius: 8px; background-color: white; cursor: pointer; outline: none; }
.input-area { display: flex; justify-content: flex-end; }
.amount-input { width: 100%; border: none; background: transparent; font-size: 2.5rem; font-weight: 800; text-align: right; color: #111827; outline: none; padding: 0; }
.result-text { color: #3b82f6; }
/* number input 화살표 제거 */
.amount-input::-webkit-outer-spin-button, .amount-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

.swap-icon-wrapper { position: relative; height: 20px; display: flex; justify-content: center; align-items: center; z-index: 2; }
.swap-icon { position: absolute; top: -18px; background: white; width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 1.2rem; border: 3px solid #f5f7fa; color: #6b7280; cursor: pointer; transition: transform 0.2s ease, background-color 0.2s; }
.swap-icon:hover { transform: scale(1.1); background-color: #eff6ff; color: #3b82f6; border-color: #dbeafe; }
.swap-icon:active { transform: scale(0.95); }

.rate-info { margin-top: 25px; font-size: 0.9rem; color: #6b7280; }
.info-icon { font-size: 1.1rem; }

.dashboard-layout { display: flex; flex-direction: column; gap: 24px; width: 100%; max-width: 1000px; align-items: center; }
@media (min-width: 900px) { .dashboard-layout { flex-direction: row; align-items: stretch; } .exchange-card, .chart-card { flex: 1; max-width: none; } }
.chart-card { background: white; width: 100%; max-width: 480px; padding: 40px 30px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); display: flex; flex-direction: column; justify-content: center; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.chart-header h2 { font-size: 1.4rem; font-weight: 800; color: #1a1a1a; margin: 0; }
.badge { background-color: #eff6ff; color: #3b82f6; font-weight: 700; font-size: 0.85rem; padding: 6px 12px; border-radius: 20px; }
.chart-wrapper { position: relative; height: 300px; width: 100%; }
.chart-desc { margin-top: 20px; text-align: center; color: #6b7280; font-size: 0.95rem; line-height: 1.5; }
.chart-desc strong { color: #3b82f6; }
</style>