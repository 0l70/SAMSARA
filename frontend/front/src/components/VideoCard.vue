<template>
  <div class="video-card" @click="goDetail">
    <div class="thumbnail-wrapper">
      <img :src="video.snippet.thumbnails.medium.url" alt="thumbnail" class="thumbnail">
    </div>
    
    <div class="video-info">
      <h3 class="title" v-html="decodedTitle"></h3>
      <div class="meta">
        <span class="channel">{{ video.snippet.channelTitle }}</span>
        <span class="date">{{ formattedDate }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  video: { type: Object, required: true }
})

const router = useRouter()

// HTML 엔티티(&amp; 등) 해독
const decodedTitle = computed(() => {
  const txt = document.createElement('textarea')
  txt.innerHTML = props.video.snippet.title
  return txt.value
})

const formattedDate = computed(() => {
  const date = new Date(props.video.snippet.publishedAt)
  return date.toLocaleDateString()
})

const goDetail = () => {
  const videoId = props.video.id.videoId
  router.push({ name: 'video-detail', params: { id: videoId } })
}
</script>

<style scoped>
.video-card {
  background-color: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px var(--shadow-color);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.video-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px var(--shadow-color);
}

.thumbnail-wrapper {
  position: relative;
  padding-top: 56.25%; /* 16:9 비율 유지 */
  overflow: hidden;
  background: #000;
}

.thumbnail {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-info {
  padding: 15px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  background-color: var(--bg-card);
}

.title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 10px;
  line-height: 1.4;
  color: var(--text-primary);

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}


.meta {
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--text-secondary);
}

.channel {
  font-weight: 500;
  color: var(--text-secondary);
}

[data-theme="dark"] .video-card {
  background-color: #1f2937;
}

[data-theme="dark"] .title {
  color: #f9fafb;
}

[data-theme="dark"] .meta,
[data-theme="dark"] .channel {
  color: #d1d5db;
}

</style>