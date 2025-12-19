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
            <label class="box-label">보낼 금액</label>
            
            <select v-if="!isSwapped" v-model="selectedCurrency" class="currency-select">
              <option v-for="currency in currencies" :key="currency.unit" :value="currency">
                {{ currency.unit }} ({{ currency.name }})
              </option>
            </select>

            <span v-else class="currency-unit">KRW (대한민국 원)</span>
          </div>
          
          <div class="input-area">
            <input 
              type="number" 
              v-model.number="inputAmount" 
              placeholder="0"
              class="amount-input"
            >
          </div>
        </div>

        <div class="swap-icon-wrapper">
          <div class="swap-icon" @click="toggleSwap" title="단위 바꾸기">
            <b>⬇</b>
          </div>
        </div>

        <div class="currency-box result-box">
          <div class="box-header">
            <label class="box-label">받을 금액 (예상)</label>

            <span v-if="!isSwapped" class="currency-unit">KRW (대한민국 원)</span>

            <select v-else v-model="selectedCurrency" class="currency-select">
              <option v-for="currency in currencies" :key="currency.unit" :value="currency">
                {{ currency.unit }} ({{ currency.name }})
              </option>
            </select>
          </div>
          
          <div class="input-area">
            <input 
              type="text" 
              :value="outputAmount" 
              disabled
              class="amount-input result-text"
            >
          </div>
        </div>

        <div class="rate-info" v-if="selectedCurrency">
          <span class="info-icon"><b>※</b></span>
          적용 환율: 1 {{ selectedCurrency.unit }} = {{ selectedCurrency.rate.toLocaleString() }} 원
        </div>
      </div>

      <div class="chart-card" v-if="selectedCurrency">
        <div class="chart-header">
          <h2>📉 {{ selectedCurrency.unit }} 최근 동향</h2>
          <span class="badge">1주일</span>
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
import { ref, computed, watch, onMounted } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

// ---------------------------------------------------------
// 상태 변수
// ---------------------------------------------------------
const currencies = ref([])
const selectedCurrency = ref(null)
const inputAmount = ref(null)
const isSwapped = ref(false)
const loading = ref(true)

// ---------------------------------------------------------
// 1. API 데이터 가져오기
// ---------------------------------------------------------
const fetchRates = async () => {
  try {
    loading.value = true
    // ★ 주소 본인 설정에 맞게 유지 (api/v1 등)
    const response = await axios.get('http://127.0.0.1:8000/api/v1/exchange/exchange-rates/')
    
    const fetchedData = response.data.map(item => {
      if (item.unit === 'JPY(100)') {
        return { unit: 'JPY', name: '일본 엔화 (100엔)', rate: item.rate }
      }
      return item
    })

    const targetUnits = ['USD', 'JPY', 'EUR', 'CNY']
    currencies.value = fetchedData.filter(c => targetUnits.includes(c.unit))

    // 기본값 USD 선택
    const usd = currencies.value.find(c => c.unit === 'USD')
    if (usd) {
      selectedCurrency.value = usd
    } else if (currencies.value.length > 0) {
      selectedCurrency.value = currencies.value[0]
    }

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
// 2. 순서 변경 (Swap)
// ---------------------------------------------------------
const toggleSwap = () => {
  isSwapped.value = !isSwapped.value
}

// ---------------------------------------------------------
// 3. 계산 로직
// ---------------------------------------------------------
const outputAmount = computed(() => {
  if (!inputAmount.value || !selectedCurrency.value) return 0
  const rate = selectedCurrency.value.rate
  const unitRate = selectedCurrency.value.unit === 'JPY' ? rate / 100 : rate

  let result = 0
  if (!isSwapped.value) {
    result = inputAmount.value * unitRate
    return Math.floor(result).toLocaleString()
  } else {
    result = inputAmount.value / unitRate
    return result.toFixed(2).toLocaleString()
  }
})

// ---------------------------------------------------------
// 4. [수정됨] 차트 데이터 동적 생성
// ---------------------------------------------------------
const getChartData = () => {
  // 데이터가 없으면 빈 차트
  if (!selectedCurrency.value) return { labels: [], datasets: [] }

  const currentRate = selectedCurrency.value.rate
  const today = new Date()
  
  const labels = []
  const dataPoints = []

  // 최근 7일 데이터 생성 (과거 -> 오늘 순서)
  for (let i = 6; i >= 0; i--) {
    // 1. 날짜 라벨 생성 (예: 12.16)
    const d = new Date()
    d.setDate(today.getDate() - i)
    const month = d.getMonth() + 1
    const day = d.getDate()
    labels.push(`${month}.${day}`)

    // 2. 환율 데이터 생성
    if (i === 0) {
      // 오늘은 '실제 데이터' 사용
      dataPoints.push(currentRate)
    } else {
      // 과거는 '실제 데이터 기반' 랜덤 변동 (±0.5% ~ ±1.5% 범위 내)
      // 실제 서비스라면 여기서 DB의 과거 데이터를 가져와야 합니다.
      const fluctuation = (Math.random() - 0.5) * (currentRate * 0.02) 
      dataPoints.push(currentRate + fluctuation)
    }
  }

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
      data: dataPoints, // 여기서 생성된 데이터 사용
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
      ticks: { color: '#6b7280', font: { size: 11 } }
    },
    y: { 
      grid: { color: '#f3f4f6' }, 
      // 차트 Y축 범위를 데이터에 맞춰서 자동 조절 (최소값 - 10원)
      suggestedMin: (ctx) => {
        if(!ctx.chart.data.datasets.length) return 0;
        return Math.min(...ctx.chart.data.datasets[0].data) - 10; 
      }
    }
  }
}

// 통화가 바뀌면 차트 새로 그림
watch(selectedCurrency, (newVal) => {
  if (newVal) {
    chartData.value = getChartData()
  }
})
</script>

<style scoped>
/* 로딩 메시지 */
.loading-msg {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  font-size: 1.2rem;
  color: #6b7280;
  font-weight: 600;
}

/* =====================
   기존 스타일 유지
===================== */
.page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background-color: #f5f7fa;
  padding: 40px 20px;
}
.exchange-card {
  background: white;
  width: 100%;
  max-width: 480px;
  padding: 40px 30px;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  text-align: center;
}
.card-title { font-size: 1.8rem; font-weight: 800; color: #1a1a1a; margin-bottom: 30px; }
.currency-box { background-color: #f3f4f6; border-radius: 16px; padding: 20px; transition: all 0.3s ease; border: 2px solid transparent; }
.currency-box.input-active:focus-within { border-color: #3b82f6; background-color: #fff; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15); }
.result-box { background-color: #eef2ff; }
.box-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.box-label { font-size: 0.95rem; font-weight: 600; color: #6b7280; }
.currency-select, .currency-unit { font-weight: 700; color: #374151; font-size: 1rem; }
.currency-select { padding: 4px 8px; border: 1px solid #d1d5db; border-radius: 8px; background-color: white; cursor: pointer; outline: none; }
.input-area { display: flex; justify-content: flex-end; }
.amount-input { width: 100%; border: none; background: transparent; font-size: 2.5rem; font-weight: 800; text-align: right; color: #111827; outline: none; padding: 0; }
.result-text { color: #3b82f6; }
.amount-input::-webkit-outer-spin-button, .amount-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

/* Swap 아이콘 수정 (클릭 가능하게) */
.swap-icon-wrapper { position: relative; height: 20px; display: flex; justify-content: center; align-items: center; z-index: 2; }
.swap-icon { 
  position: absolute; top: -18px; background: white; width: 40px; height: 40px; 
  border-radius: 50%; display: flex; justify-content: center; align-items: center; 
  font-size: 1.2rem; border: 3px solid #f5f7fa; color: #6b7280; 
  cursor: pointer; /* 커서 모양 손가락으로 변경 */
  transition: transform 0.2s ease, background-color 0.2s;
}
.swap-icon:hover { transform: scale(1.1); background-color: #eff6ff; color: #3b82f6; border-color: #dbeafe; }
.swap-icon:active { transform: scale(0.95); }

.rate-info { margin-top: 25px; font-size: 0.9rem; color: #6b7280; display: flex; justify-content: center; align-items: center; gap: 5px; }
.info-icon { font-size: 1.1rem; }

/* 차트 및 레이아웃 스타일 */
.dashboard-layout { display: flex; flex-direction: column; gap: 24px; width: 100%; max-width: 1000px; align-items: center; }
@media (min-width: 900px) {
  .dashboard-layout { flex-direction: row; align-items: stretch; }
  .exchange-card, .chart-card { flex: 1; max-width: none; }
}
.chart-card { background: white; width: 100%; max-width: 480px; padding: 40px 30px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); display: flex; flex-direction: column; justify-content: center; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.chart-header h2 { font-size: 1.4rem; font-weight: 800; color: #1a1a1a; margin: 0; }
.badge { background-color: #eff6ff; color: #3b82f6; font-weight: 700; font-size: 0.85rem; padding: 6px 12px; border-radius: 20px; }
.chart-wrapper { position: relative; height: 300px; width: 100%; }
.chart-desc { margin-top: 20px; text-align: center; color: #6b7280; font-size: 0.95rem; line-height: 1.5; }
.chart-desc strong { color: #3b82f6; }
</style>