<template>
  <div class="page-container">
    
    <div class="header-section">
      <span class="badge-title">원자재 시장</span>
      
      <h1 class="page-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#d4af37" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="header-icon">
          <path d="M6 10L8 6H16L18 10H6Z" />
          <path d="M6 10V18C6 19.1 6.9 20 8 20H16C17.1 20 18 19.1 18 18V10" />
          <path d="M20 14L23 11L20 8" stroke="#f57f17" />
          <path d="M12 11L23 11" stroke="#f57f17" />
        </svg>
        금/은 시세
      </h1>
      
      <p class="page-subtitle">실시간 국제 시세와 환율을 반영한 차트입니다.</p>
    </div>

    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>데이터를 불러오는 중...</p>
    </div>

    <div v-else class="dashboard-layout">
      <div class="chart-card full-width">
        
        <div class="card-header">
          
          <div class="header-left">
            <div class="metal-tabs">
              <button 
                @click="selectedMetal = 'gold'" 
                :class="['tab-btn', { active: selectedMetal === 'gold', 'gold-active': selectedMetal === 'gold' }]"
              >
                금 (Gold)
              </button>
              <button 
                @click="selectedMetal = 'silver'" 
                :class="['tab-btn', { active: selectedMetal === 'silver', 'silver-active': selectedMetal === 'silver' }]"
              >
                은 (Silver)
              </button>
            </div>

            <p class="rate-text">
              적용 환율: <strong>1$ = {{ currentExchangeRate.toLocaleString() }}원</strong>
            </p>
          </div>

          <div class="header-right">
            <span class="price-label">
              현재 {{ selectedMetal === 'gold' ? '금' : '은' }}값 (Live)
            </span>
            
            <div class="big-price-box">
              <span :class="['currency', selectedMetal === 'gold' ? 'text-gold' : 'text-silver']">₩</span>
              
              <strong :class="['big-price', selectedMetal === 'gold' ? 'text-gold' : 'text-silver']">
                {{ selectedMetal === 'gold' ? currentGoldPrice.toLocaleString() : currentSilverPrice.toLocaleString() }}
              </strong>
              
              <span class="unit">/g</span>
            </div>
          </div>
        </div>

        <div class="chart-wrapper">
          <Line v-if="isLoaded" :data="chartData" :options="chartOptions" />
        </div>
        
        <p class="chart-desc">
          ※ 데이터 출처: 한국수출입은행 환율 API 기반 계산
        </p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

// ==========================================
// 1. 상태 변수 정의
// ==========================================
const TROY_OZ_TO_G = 31.1035 // 1온스 = 31.1035g
const currentExchangeRate = ref(1400) // 환율 기본값 (로딩 전)
const selectedMetal = ref('gold') // 👈 'gold' 또는 'silver' (현재 선택된 탭)
const currentGoldPrice = ref(0) // 👈 현재 금값을 저장할 변수
const currentSilverPrice = ref(0) // 👈 은값 저장용 변수 추가

const chartData = ref({ labels: [], datasets: [] })
const chartOptions = ref({})
const isLoading = ref(true)
const isLoaded = ref(false)

// ==========================================
// 2. 환율 정보 가져오기 (계산기와 동일한 API 사용)
// ==========================================
const fetchUsdRate = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/exchange/exchange-rates/')
    const rates = res.data

    if (!rates || rates.length === 0) return

    // 👇 [수정 핵심] 'cur_unit' 대신 'unit'을 사용해야 합니다!
    const usdData = rates.find(r => r.unit === 'USD')

    if (usdData) {
      // 👇 [수정 핵심] 'deal_bas_r' 대신 'rate'를 사용해야 합니다!
      // 이미 숫자로 들어오고 있다면 parseFloat이나 replace가 필요 없을 수도 있지만,
      // 혹시 문자열일 경우를 대비해 안전하게 처리합니다.
      
      const rateValue = usdData.rate
      
      // 만약 rate가 "1,440.5" 같은 문자열이라면 콤마 제거 후 변환
      if (typeof rateValue === 'string') {
          currentExchangeRate.value = parseFloat(rateValue.replace(/,/g, ''))
      } else {
          // 숫자라면 그대로 사용
          currentExchangeRate.value = rateValue
      }
    } else {
      console.warn('USD 데이터를 찾을 수 없습니다.')
    }
  } catch (error) {
    console.error('환율 로딩 에러:', error)
  }
}

// 3. 금/은 시세 가져오기 함수 수정
const fetchGoldPrice = async () => {
  try {
    isLoading.value = true
    
    await fetchUsdRate() // 환율 가져오기
    
    const res = await axios.get('http://127.0.0.1:8000/api/v1/exchange/gold-silver/')
    const data = res.data

    if (!data || data.length === 0) {
      alert("데이터가 없습니다.")
      return
    }

    // 날짜 처리 (기존 코드)
    const dates = data.map(d => {
        const dateObj = new Date(d.date)
        return `${dateObj.getMonth() + 1}.${dateObj.getDate()}`
    })
    
    // 계산 로직 (기존 코드)
    const goldPrices = data.map(d => Math.round((d.gold * currentExchangeRate.value) / TROY_OZ_TO_G))
    const silverPrices = data.map(d => Math.round((d.silver * currentExchangeRate.value) / TROY_OZ_TO_G))

    // 🌟 [추가됨] 가장 마지막(최신) 금값을 변수에 저장
    if (goldPrices.length > 0) {
        currentGoldPrice.value = goldPrices[goldPrices.length - 1]
        currentSilverPrice.value = silverPrices[silverPrices.length - 1]
    }
    // ④ 차트 데이터 구성
    chartData.value = {
      labels: dates,
      datasets: [
        {
          label: '금 (Gold)',
          backgroundColor: (ctx) => {
            const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 400)
            gradient.addColorStop(0, 'rgba(255, 215, 0, 0.4)')
            gradient.addColorStop(1, 'rgba(255, 215, 0, 0.0)')
            return gradient
          },
          borderColor: '#d4af37',
          borderWidth: 2,
          data: goldPrices,
          yAxisID: 'y',
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: '#fff',
          pointBorderColor: '#d4af37',
        },
        {
          label: '은 (Silver)',
          backgroundColor: (ctx) => {
            const gradient = ctx.chart.ctx.createLinearGradient(0, 0, 0, 400)
            gradient.addColorStop(0, 'rgba(192, 192, 192, 0.4)')
            gradient.addColorStop(1, 'rgba(192, 192, 192, 0.0)')
            return gradient
          },
          borderColor: '#a0a0a0',
          borderWidth: 2,
          data: silverPrices,
          yAxisID: 'y1',
          fill: true,
          tension: 0.4,
          pointRadius: 3,
          pointBackgroundColor: '#fff',
          pointBorderColor: '#a0a0a0',
        }
      ]
    }
    
    // 차트 옵션 설정
    chartOptions.value = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', labels: { usePointStyle: true, font: { family: "'Noto Sans KR'" } } },
        tooltip: {
            backgroundColor: 'rgba(0,0,0,0.8)',
            padding: 10,
            cornerRadius: 8,
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) label += ': ';
                    if (context.parsed.y !== null) label += '₩' + context.parsed.y.toLocaleString();
                    return label;
                }
            }
        }
      },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#888' } },
        y: {
          type: 'linear', display: true, position: 'left',
          title: { display: true, text: '금 (₩/g)', color: '#d4af37', font:{weight:'bold'} },
          grid: { color: '#f0f0f0' },
          ticks: { color: '#666', callback: (v) => '₩' + v.toLocaleString() }
        },
        y1: {
          type: 'linear', display: true, position: 'right',
          title: { display: true, text: '은 (₩/g)', color: '#a0a0a0', font:{weight:'bold'} },
          grid: { drawOnChartArea: false },
          ticks: { color: '#666', callback: (v) => '₩' + v.toLocaleString() }
        },
      }
    }
    
    isLoaded.value = true
  } catch (error) {
    console.error('로딩 실패:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchGoldPrice()
})
</script>
<style scoped>
/* =====================
  1. 전체 레이아웃 및 배경
===================== */
.page-container { 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  min-height: 80vh; 
  background-color: var(--bg-body); /* 배경 변수 */
  padding: 60px 20px; 
  transition: background-color 0.3s ease;
}

.header-section { text-align: center; margin-bottom: 30px; }

.badge-title { 
  background-color: var(--bg-badge); /* 다크모드 대응 뱃지 배경 */
  color: #f57f17; 
  font-weight: 700; 
  padding: 6px 12px; 
  border-radius: 20px; 
  font-size: 0.85rem; 
  margin-bottom: 10px; 
  display: inline-block; 
}

.page-title { 
  font-size: 2rem; 
  font-weight: 800; 
  color: var(--text-primary); /* 텍스트 변수 */
  margin: 0 0 5px 0; 
}

.page-subtitle { 
  color: var(--text-secondary); /* 텍스트 변수 */
  font-size: 1rem; 
  margin: 0; 
}

/* =====================
  2. 카드 및 헤더 레이아웃
===================== */
.dashboard-layout { width: 100%; max-width: 1000px; }

.chart-card { 
  background: var(--bg-card); /* 카드 배경 변수 */
  padding: 30px; 
  border-radius: 24px; 
  box-shadow: 0 10px 30px var(--shadow-color);
  border: 1px solid var(--border-color); /* 테두리 추가 */
  transition: background-color 0.3s ease;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 2px solid var(--border-color); /* 경계선 변수 */
}

/* =====================
   2. 헤더 섹션 (레퍼런스 스타일 적용)
===================== */
.header-section {
  text-align: center;
  margin-bottom: 40px;
}

.badge-title {
  background-color: var(--bg-badge); /* 기존 변수 활용 */
  color: #d4af37; /* 금색 텍스트 */
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
  
  /* ★ 핵심: 아이콘과 텍스트 가로 정렬 (Flex) ★ */
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

/* 아이콘 미세 조정 */
.header-icon {
  color: #d4af37; /* 금색 */
  filter: drop-shadow(0 2px 4px rgba(212, 175, 55, 0.2)); /* 살짝 빛나는 효과 */
  transform: translateY(-2px); /* 시각적 중심 맞춤 */
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

/* 모바일 대응 */
@media (max-width: 600px) {
  .page-title {
    font-size: 1.8rem;
    gap: 8px;
  }
  .header-icon {
    width: 28px;
    height: 28px;
  }
}

/* =====================
  3. 토글 탭 버튼 (가시성 강화)
===================== */
.metal-tabs {
  background-color: var(--bg-body); /* 배경색과 맞춤 */
  padding: 5px;
  border-radius: 16px;
  display: inline-flex;
  width: fit-content;
  border: 1px solid var(--border-color);
}

.tab-btn {
  border: none;
  background: transparent;
  color: var(--text-muted);
  padding: 10px 24px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

/* 활성화된 버튼 스타일 */
.tab-btn.active {
  background-color: var(--bg-card); /* 선택된 버튼은 카드색으로 */
  box-shadow: 0 4px 12px var(--shadow-color);
  transform: scale(1.02);
}

.tab-btn.gold-active { color: #d4af37; }
.tab-btn.silver-active { color: #94a3b8; } /* 다크모드에서 은색은 조금 더 밝게 */

.rate-text {
  font-size: 0.95rem;
  color: var(--text-muted);
  margin: 20px 10px 0px;
}

/* =====================
  4. 가격 표시 영역
===================== */
.header-right { text-align: right; }
.price-label { font-size: 0.95rem; color: var(--text-muted); font-weight: 600; margin-bottom: -5px; display: block; }

.big-price-box {
  display: flex;
  align-items: baseline;
  justify-content: flex-end;
  gap: 4px;
}

.big-price {
  font-size: 3.5rem;
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -1.5px;
  color: var(--text-primary);
}

.currency { 
  font-size: 1.8rem; 
  font-weight: 700; 
  color: var(--text-primary);
  transform: translateY(-8px); 
}

.unit { font-size: 1.1rem; color: var(--text-muted); font-weight: 600; }

/* 색상 유틸리티 - 다크모드에서도 빛나 보이게 글로우 살짝 추가 */
.text-gold { color: #d4af37; text-shadow: 0 0 15px rgba(212, 175, 55, 0.3); }
.text-silver { color: #cbd5e1; text-shadow: 0 0 15px rgba(203, 213, 225, 0.2); }

/* =====================
  5. 기타 요소
===================== */
.loading-container { text-align: center; margin-top: 50px; color: var(--text-muted); }
.spinner { 
  width: 40px; height: 40px; 
  border: 4px solid var(--border-color); 
  border-top: 4px solid #d4af37; 
  border-radius: 50%; 
  margin: 0 auto 20px; 
  animation: spin 1s linear infinite; 
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.chart-wrapper { position: relative; height: 450px; width: 100%; }
.chart-desc { margin-top: 20px; text-align: center; color: var(--text-muted); font-size: 0.8rem; }

/* 모바일 대응 */
@media (max-width: 700px) {
  .card-header { flex-direction: column; align-items: flex-start; gap: 25px; }
  .header-right { 
    width: 100%; text-align: left; 
    border-left: 5px solid var(--border-color); 
    padding-left: 20px; 
  }
  .big-price-box { justify-content: flex-start; }
  .big-price { font-size: 2.8rem; }
}
</style>