<template>
  <button 
    :class="['kakao-btn', type === 'icon' ? 'btn-icon' : 'btn-full']" 
    @click="kakaoLogin"
  >
    <svg viewBox="0 0 24 24" fill="currentColor" class="kakao-logo">
      <path d="M12 3C5.9 3 1 6.9 1 11.8c0 3.1 2 5.9 5 7.5-.2.8-1 2.9-1.1 3.2-.2.4.1.6.4.4.2-.1 3.2-2.2 4.4-3 .7.1 1.4.2 2.2.2 6.1 0 11-3.9 11-8.8C23 6.9 18.1 3 12 3z"/>
    </svg>
    
    <span v-if="type !== 'icon'" class="btn-text">
      카카오 로그인
    </span>
  </button>
</template>

<script setup>
// 부모 컴포넌트에서 type을 받아옵니다. (기본값: 'full')
const props = defineProps({
  type: {
    type: String,
    default: 'full' // 'full' 또는 'icon'
  }
})

const kakaoLogin = () => {
  window.Kakao.Auth.authorize({
    // redirectUri: 'http://localhost:5173/oauth/callback/kakao' 
    redirectUri: 'http://61.73.128.241:5173/oauth/callback/kakao' 
  })
}
</script>

<style scoped>
/* 공통 스타일: 카카오 노란색 배경 */
.kakao-btn {
  background-color: #FEE500; /* 카카오 공식 컬러 */
  color: #191919;            /* 카카오 공식 텍스트 컬러 (진한 검정) */
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  padding: 0;
}

.kakao-btn:hover {
  background-color: #fdd835; /* 호버 시 약간 진해짐 */
  transform: translateY(-2px); /* 살짝 떠오르는 효과 */
}

/* 1. 꽉 찬 버튼 (Full Width) 스타일 */
.btn-full {
  width: 100%;       /* 부모 너비에 맞춤 */
  height: 50px;      /* 파란 버튼과 높이 동일하게 설정 */
  border-radius: 12px; /* 파란 버튼과 모서리 둥글기 맞춤 (6px -> 12px 추천) */
  font-size: 1rem;
  font-weight: 700;  /* 글자 굵게 */
  gap: 8px;          /* 로고와 글자 사이 간격 */
}

/* 2. 아이콘 버튼 (Mini) 스타일 */
.btn-icon {
  width: 44px;       /* 정사각형 크기 */
  height: 44px;
  border-radius: 12px; /* 둥근 사각형 (원형을 원하면 50%로 변경) */
}

/* 로고 스타일 */
.kakao-logo {
  width: 20px;
  height: 20px;
}

/* 텍스트 스타일 */
.btn-text {
  margin-top: 1px; /* 시각적 중앙 정렬 보정 */
}
</style>