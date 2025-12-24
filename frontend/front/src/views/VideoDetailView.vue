<template>
  <div class="detail-page">
    <div class="content-wrapper">
      
      <div class="detail-header">
        <span class="category">YouTube Player</span>
        <h2>영상 재생</h2>
      </div>
      
      <div class="video-container">
        <div class="video-frame shadow-effect">
          <iframe 
            :src="videoUrl" 
            title="YouTube video player" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen
          ></iframe>
        </div>
      </div>

      <div class="control-area">
        <button @click="goBack" class="btn-back">
          <span class="arrow">←</span> 목록으로 돌아가기
        </button>
      </div>
      
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const videoId = route.params.id

const videoUrl = computed(() => {
  return `https://www.youtube.com/embed/${videoId}`
})

const goBack = () => {
  router.back()
}
</script>

<style scoped>
/* =====================
  1. 전체 레이아웃
===================== */
.detail-page {
  min-height: 90vh;
  /* 라이트: #f5f7fa, 다크: var(--bg-body) */
  background-color: var(--bg-body); 
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  transition: background-color 0.3s ease;
}

.content-wrapper {
  width: 100%;
  max-width: 900px;
}

/* =====================
  2. 헤더 스타일
===================== */
.detail-header {
  text-align: center;
  margin-bottom: 30px;
}

.category {
  font-size: 0.85rem;
  color: #3182f6; /* 브랜드 컬러 유지 */
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

h2 {
  font-size: 2rem;
  /* 라이트: #111, 다크: var(--text-primary) */
  color: var(--text-primary);
  margin-top: 5px;
  font-weight: 800;
}

/* =====================
  3. 비디오 컨테이너 (시네마틱 효과)
===================== */
.video-container {
  position: relative;
  width: 100%;
  margin-bottom: 40px;
}

.video-frame {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
  border-radius: 20px;
  background-color: #000; /* 비디오 로딩 전 검은 배경 유지 */
}

/* 그림자 효과 - 다크모드에서는 더 깊고 진한 그림자 사용 */
.shadow-effect {
  box-shadow: 
    0 20px 40px -10px var(--shadow-color), 
    0 0 0 1px var(--border-color); /* 미세한 테두리 변수 적용 */
}

.video-frame iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}

/* =====================
  4. 버튼 영역 (다크모드 대응 알약 버튼)
===================== */
.control-area {
  display: flex;
  justify-content: center;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  /* 라이트: white, 다크: var(--bg-card) */
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 700;
  /* 라이트: #495057, 다크: var(--text-secondary) */
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px var(--shadow-color);
}

.btn-back:hover {
  /* 호버 시 더 밝아지거나 색상 변경 */
  background-color: var(--bg-hover); 
  transform: translateY(-2px);
  box-shadow: 0 6px 12px var(--shadow-color);
  color: #3182f6; /* 호버 시 텍스트 파란색 강조 */
}

.arrow {
  font-size: 1.2rem;
  transition: transform 0.2s;
}

.btn-back:hover .arrow {
  transform: translateX(-3px);
}
</style>