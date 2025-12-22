<template>
  <div class="detail-container">
    <h2>영상 상세 재생</h2>
    
    <div class="video-wrapper">
      <iframe 
        :src="videoUrl" 
        title="YouTube video player" 
        frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen
      ></iframe>
    </div>

    <div class="btn-area">
      <button @click="goBack" class="btn-back">목록으로 돌아가기</button>
      </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// URL 파라미터에서 영상 ID 가져오기 (router/index.js의 :id 부분)
const videoId = route.params.id

// 유튜브 임베드(퍼가기) URL 생성
const videoUrl = computed(() => {
  return `https://www.youtube.com/embed/${videoId}`
})

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 30px auto;
  padding: 20px;
  text-align: center;
}

/* 반응형 비디오 (16:9 비율 유지) */
.video-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
  background-color: #000;
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.btn-area {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.btn-back {
  padding: 10px 20px;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}
.btn-back:hover {
  background-color: #e9ecef;
}
</style>