<template>
  <div class="hero">
    <h1>라고 할 때 살걸...</h1>
    <p>예적금 금리 비교부터 환율 계산까지,</p>
    <p>살 걸 후회하지 마세요</p>
  </div>
</template>

<script setup>
// 특별한 로직 없음
</script>

<style scoped>
.hero {
  text-align: center;
  margin-top: 100px;
}

h1 { 
  font-size: 3rem; 
  /* 라이트: #2c3e50, 다크: var(--text-primary) */
  color: var(--text-primary); 
  margin-bottom: 20px; 
  transition: color 0.3s ease;
}

p { 
  font-size: 1.2rem; 
  /* 라이트: #666, 다크: var(--text-secondary) */
  color: var(--text-secondary); 
  transition: color 0.3s ease;
}
</style>