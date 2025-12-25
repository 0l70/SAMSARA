<template>
  <div class="search-container">
    <div class="header-section">
      <h1>금융 영상 검색</h1>
      <p class="subtitle">어려운 금융 공부, 영상으로 쉽게 시작하세요.</p>
      
      <div class="search-box">
        <input 
          type="text" 
          v-model="keyword" 
          @keyup.enter="searchVideos"
          placeholder="검색어를 입력하세요 (예: 적금 추천)"
          class="search-input"
        >
        <button @click="searchVideos" class="search-btn">
          검색
        </button>
      </div>
    </div>

    <div v-if="videos.length > 0" class="video-grid">
      <VideoCard 
        v-for="video in videos" 
        :key="video.id.videoId" 
        :video="video" 
      />
    </div>
    
    <div v-else-if="searched" class="no-result">
      <p>검색 결과가 없습니다. 다른 검색어로 시도해보세요!</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import VideoCard from '@/components/VideoCard.vue'

const keyword = ref('')
const videos = ref([])
const searched = ref(false)
const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
const API_URL = 'https://www.googleapis.com/youtube/v3/search'

// ✅ 스마트 필터링을 위한 '금융 필수 키워드' 리스트 정의
const financeKeywords = [
  '금융', '주식', '경제', '재테크', '증권', '은행', '적금', '예금', '투자', '코인', '비트코인', 
  '부동산', '청약', '금리', '환율', 'ETF', '배당', '노후', '연금', '세금', '절세', '삼성전자', 
  '시황', '뉴스', '매매', '차트', '부자', '자산', '빚', '대출', '신용', '보험', 'market', 'stock', 'invest'
]

const searchVideos = async () => {
  const query = keyword.value.trim()

  // 1. 유효성 검사 (2글자 미만 차단)
  if (query.length < 2) {
    alert('검색어는 최소 두 글자 이상 입력해야 합니다!')
    return
  }

  try {
    const res = await axios.get(API_URL, {
      params: {
        key: API_KEY,
        part: 'snippet',
        maxResults: 20, // 필터링으로 걸러질 것을 대비해 평소보다 많이(20개) 가져옵니다.
        type: 'video',
        q: `${query} 금융 경제 주식 재테크`, // 1차: 유튜브에게 요청
        order: 'relevance',
        videoDuration: 'medium',
      }
    })

    // 2. [핵심 로직] 스마트 필터링 (화이트리스트 검사)
    const filteredVideos = res.data.items.filter(video => {
      const title = video.snippet.title.toLowerCase()
      const description = video.snippet.description.toLowerCase()
      
      // 제목이나 설명에 '금융 필수 키워드'가 하나라도 포함되어 있는지 확인
      const hasFinanceKeyword = financeKeywords.some(k => 
        title.includes(k) || description.includes(k)
      )
      
      return hasFinanceKeyword
    })

    // 3. 결과 반영
    videos.value = filteredVideos
    searched.value = true

  } catch (error) {
    console.error('API Error:', error)
    alert('검색 중 오류가 발생했습니다.')
  }
}
</script>

<style scoped>
/* =====================
  1. 전체 레이아웃 및 배경
===================== */
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: var(--bg-body); /* 배경 변수 적용 */
  min-height: 100vh;
  transition: background-color 0.3s ease;
}

.header-section {
  text-align: center;
  margin-bottom: 50px;
}

/* =====================
  2. 폰트 컬러 (다크모드 대응)
===================== */
h1 {
  font-size: 2.5rem;
  /* 라이트: #2c3e50, 다크: var(--text-primary) */
  color: var(--text-primary);
  margin-bottom: 10px;
  font-weight: 800;
}

.subtitle {
  /* 라이트: #666, 다크: var(--text-secondary) */
  color: var(--text-secondary);
  margin-bottom: 30px;
}

/* =====================
  3. 검색창 스타일 (디자인 유지 + 다크모드 가시성)
===================== */
.search-box {
  display: flex;
  max-width: 600px;
  margin: 0 auto;
  /* 다크모드에서는 그림자를 더 깊게 조정 */
  box-shadow: 0 4px 15px var(--shadow-color);
  border-radius: 50px;
  overflow: hidden;
  /* 라이트: #eee, 다크: var(--border-color) */
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  transition: all 0.3s ease;
}

.search-input {
  flex: 1;
  padding: 15px 25px;
  border: none;
  font-size: 16px;
  outline: none;
  background: transparent; /* 부모인 search-box 배경색을 따름 */
  color: var(--text-primary);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-btn {
  background-color: #3182f6; /* 포인트 컬러 유지 */
  color: white;
  border: none;
  padding: 0 30px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.search-btn:hover {
  background-color: #2372e0;
}

/* =====================
  4. 그리드 및 결과 메시지
===================== */
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

.no-result {
  text-align: center;
  color: var(--text-muted); /* #999 대신 변수 사용 */
  margin-top: 50px;
  font-size: 1.2rem;
}

</style>