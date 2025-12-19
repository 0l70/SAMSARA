<template>
  <div class="gold-container">
    <h1>✨ 국제 금/은 선물 시세 (1개월)</h1>
    
    <div v-if="isLoading" class="loading">
      데이터를 불러오는 중입니다... ⏳
    </div>

    <div v-else class="chart-wrapper">
      <Line v-if="isLoaded" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

// 1. Chart.js 필수 요소 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// 2. 상태 변수들
const chartData = ref({ labels: [], datasets: [] })
const chartOptions = ref({})
const isLoading = ref(true)
const isLoaded = ref(false)

// 3. 데이터 가져오는 함수
const fetchGoldPrice = async () => {
  try {
    isLoading.value = true
    
    // 🔥 백엔드 주소 확인 필수! (본인 urls.py 설정에 맞게 수정)
    // 예: http://127.0.0.1:8000/exchange/gold-silver/ 일 수도 있음
    const res = await axios.get('http://127.0.0.1:8000/api/v1/exchange/gold-silver/')
    const data = res.data
    
    console.log("받아온 데이터:", data)

    // 데이터가 비었을 경우 처리
    if (!data || data.length === 0) {
      alert("데이터가 없습니다.")
      return
    }

    // 데이터 분리
    const dates = data.map(d => d.date)
    const goldPrices = data.map(d => d.gold)
    const silverPrices = data.map(d => d.silver)

    // 차트 데이터 설정
    chartData.value = {
      labels: dates,
      datasets: [
        {
          label: '금 선물 (USD/oz)',
          backgroundColor: 'rgba(255, 215, 0, 0.2)', // 금색 배경
          borderColor: '#FFD700', // 금색 선
          data: goldPrices,
          yAxisID: 'y',
          tension: 0.3 // 부드러운 곡선
        },
        {
          label: '은 선물 (USD/oz)',
          backgroundColor: 'rgba(192, 192, 192, 0.2)', // 은색 배경
          borderColor: '#C0C0C0', // 은색 선
          data: silverPrices,
          yAxisID: 'y1',
          tension: 0.3
        }
      ]
    }
    
    // 차트 옵션 설정 (축 2개 사용)
    chartOptions.value = {
      responsive: true,
      maintainAspectRatio: false, // 높이 조절을 위해 false
      interaction: {
        mode: 'index',
        intersect: false,
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: { display: true, text: '금 시세 ($)' }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: { display: true, text: '은 시세 ($)' },
          grid: { drawOnChartArea: false }, // 오른쪽 그리드 숨김
        },
      }
    }
    
    isLoaded.value = true
  } catch (error) {
    console.error('데이터 로딩 실패:', error)
    alert("데이터를 불러오지 못했습니다. 백엔드 서버를 확인하세요.")
  } finally {
    isLoading.value = false
  }
}

// 4. 컴포넌트 마운트 시 실행
onMounted(() => {
  fetchGoldPrice()
})
</script>

<style scoped>
.gold-container {
  max-width: 1000px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
}

/* 차트 높이 지정 (중요) */
.chart-wrapper {
  position: relative;
  height: 500px; 
  width: 100%;
  margin-top: 30px;
  background-color: #f8f9fa; /* 연한 회색 배경 */
  border-radius: 10px;
  padding: 10px;
}

.loading {
  font-size: 1.5rem;
  margin-top: 50px;
  color: #666;
  font-weight: bold;
}
</style>