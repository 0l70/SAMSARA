import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', () => {
  // localStorage에서 가져오거나 기본값 'light'
  const isDark = ref(localStorage.getItem('theme') === 'dark')

  // 초기 실행 시 태그 설정
  if (isDark.value) {
    document.documentElement.setAttribute('data-theme', 'dark')
  } else {
    document.documentElement.setAttribute('data-theme', 'light')
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    const theme = isDark.value ? 'dark' : 'light'
    
    // ✨ 이 부분이 핵심입니다! HTML 태그에 속성을 심어줘야 CSS가 인식합니다.
    document.documentElement.setAttribute('data-theme', theme)
    localStorage.setItem('theme', theme)
  }

  return { isDark, toggleTheme }
})