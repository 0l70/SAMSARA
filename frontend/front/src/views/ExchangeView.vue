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
const currencies = ref([])       // 계산기용 최신 데이터 (국가별 1개)
const currencyHistory = ref({})  // 차트용 전체 데이터 (국가별 리스트)
const selectedCurrency = ref(null)
const inputAmount = ref(null)
const isSwapped = ref(false)
const loading = ref(true)

// ---------------------------------------------------------
// 1. [수정] API 데이터 가져오기 & 분류하기
// ---------------------------------------------------------
const fetchRates = async () => {
  try {
    loading.value = true
    const response = await axios.get('http://127.0.0.1:8000/api/v1/exchange/exchange-rates/')
    const rawData = response.data

    // 1-1. 데이터 전처리 (JPY 100단위 처리 등)
    const processedData = rawData.map(item => {
      let unit = item.unit
      let name = item.name
      let rate = item.rate

      // JPY(100) 등 100단위 통화 처리
      if (unit.endsWith('(100)')) {
        unit = unit.replace('(100)', '') // 'JPY(100)' -> 'JPY'
        rate = rate / 100                // 900원 -> 9원 (1엔당)
        name = name.replace('(100)', '') // 이름에서도 제거
      }
      
      return {
        date: item.search_date, // 백엔드에서 보낸 날짜
        unit: unit,
        name: name,
        rate: rate
      }
    })

    // 1-2. 데이터 분류 (최신 데이터 vs 히스토리 데이터)
    const latestMap = new Map() // 각 통화별 최신 데이터 저장용
    const historyMap = {}       // 각 통화별 전체 기록 저장용

    processedData.forEach(item => {
      // (1) 히스토리 그룹화
      if (!historyMap[item.unit]) {
        historyMap[item.unit] = []
      }
      historyMap[item.unit].push(item)

      // (2) 최신 데이터 찾기 (날짜 비교)
      if (!latestMap.has(item.unit)) {
        latestMap.set(item.unit, item)
      } else {
        // 이미 저장된 것보다 현재 아이템이 더 최신이면 교체
        const existing = latestMap.get(item.unit)
        if (new Date(item.date) > new Date(existing.date)) {
          latestMap.set(item.unit, item)
        }
      }
    })

    // 1-3. 상태 변수에 저장
    currencyHistory.value = historyMap
    
    // 주요 통화만 필터링해서 드롭다운에 표시
    const targetUnits = ['USD', 'JPY', 'EUR', 'CNY']
    currencies.value = Array.from(latestMap.values())
      .filter(c => targetUnits.includes(c.unit))

    // 기본값 설정 (USD)
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
  
  let result = 0
  if (!isSwapped.value) {
    result = inputAmount.value * rate
    return Math.floor(result).toLocaleString()
  } else {
    result = inputAmount.value / rate
    return result.toFixed(2).toLocaleString()
  }
})

// ---------------------------------------------------------
// 4. [수정] 진짜 데이터로 차트 그리기
// ---------------------------------------------------------
const getChartData = () => {
  if (!selectedCurrency.value) return { labels: [], datasets: [] }

  const unit = selectedCurrency.value.unit
  // 해당 통화의 히스토리 가져오기
  const history = currencyHistory.value[unit] || []

  // 날짜 오름차순 정렬 (과거 -> 현재) 해야 그래프가 왼쪽에서 오른쪽으로 그려짐
  // 백엔드에서 날짜순으로 안 올 수도 있으니 안전하게 정렬
  const sortedHistory = [...history].sort((a, b) => new Date(a.date) - new Date(b.date))

  // 라벨(날짜)과 데이터(환율) 추출
  // 날짜 형식 예쁘게 변환 (2025-11-28 -> 11.28)
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
      data: dataPoints, // ★ 진짜 데이터 연결
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
      // Y축 범위 자동 조절 (데이터 최소값보다 조금 아래부터 시작)
      suggestedMin: (ctx) => {
        if(!ctx.chart.data.datasets.length) return 0;
        const values = ctx.chart.data.datasets[0].data;
        return Math.min(...values) - (Math.min(...values) * 0.005); // 최소값의 0.5% 아래 여유
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

.swap-icon-wrapper { position: relative; height: 20px; display: flex; justify-content: center; align-items: center; z-index: 2; }
.swap-icon { 
  position: absolute; top: -18px; background: white; width: 40px; height: 40px; 
  border-radius: 50%; display: flex; justify-content: center; align-items: center; 
  font-size: 1.2rem; border: 3px solid #f5f7fa; color: #6b7280; 
  cursor: pointer; 
  transition: transform 0.2s ease, background-color 0.2s;
}
.swap-icon:hover { transform: scale(1.1); background-color: #eff6ff; color: #3b82f6; border-color: #dbeafe; }
.swap-icon:active { transform: scale(0.95); }

.rate-info { margin-top: 25px; font-size: 0.9rem; color: #6b7280; }
.info-icon { font-size: 1.1rem; }

/* 차트 레이아웃 */
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