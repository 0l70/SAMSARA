<template>
  <div class="mypage-container">
    <div class="mypage-card">
      <h1>마이페이지</h1>
      <p class="subtitle">내 정보를 확인하고 수정할 수 있습니다.</p>

      <form @submit.prevent="updateProfile">
        <h3 class="section-title">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-svg">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          내 정보 수정
        </h3>

        <div class="row">
          <div class="form-group">
            <label>닉네임</label>
            <input type="text" v-model="userInfo.nickname">
          </div>
          
          <div class="form-group">
            <label>금융 MBTI</label>
            
            <div v-if="userInfo.mbti" class="mbti-display">
              <span class="mbti-result">{{ mbtiLabel }}</span>
              <button type="button" class="retest-btn" @click="goTest">
                다시 하기 ↺
              </button>
            </div>

            <div v-else class="mbti-display">
              <span class="mbti-none">아직 테스트 전입니다.</span>
              <button type="button" class="start-test-btn" @click="goTest">
                테스트 하러가기 👉
              </button>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="form-group">
            <label>나이</label>
            <input type="number" v-model.number="userInfo.age">
          </div>
          <div class="form-group">
            <label>성별</label>
            <select v-model="userInfo.gender">
              <option value="남성">남성</option>
              <option value="여성">여성</option>
            </select>
          </div>
        </div>
        
        <div class="row">
          <div class="form-group">
            <label>직업</label>
            <select v-model="userInfo.job">
              <option value="학생">학생</option>
              <option value="직장인">직장인</option>
              <option value="자영업">자영업/프리랜서</option>
              <option value="전업주부">전업주부</option>
              <option value="전문직">전문직</option>
              <option value="무직">무직/취업준비생</option>
            </select>
          </div>
          <div class="form-group">
            <label>자금 출처</label>
            <select v-model="userInfo.income_source">
              <option value="월급">월급</option>
              <option value="용돈">용돈</option>
              <option value="사업수익">사업수익</option>
              <option value="금융소득">금융소득</option>
              <option value="기타">기타</option>
            </select>
          </div>
        </div>

        <div class="agreement-box">
          <input type="checkbox" id="mydata-edit" v-model="userInfo.is_mydata_agreed">
          <label for="mydata-edit">
            <strong>마이데이터 서비스 동의</strong>
            <span class="desc">체크 시 맞춤형 상품 추천을 받을 수 있습니다.</span>
          </label>
        </div>

        <button type="submit" class="action-btn update-btn">정보 수정 저장</button>
      </form>

      <hr class="divider">

      <div class="password-section">
        <button type="button" @click="showPasswordForm = !showPasswordForm" class="toggle-btn">
          <span style="display: flex; align-items: center; gap: 8px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-svg">
              <rect x="3" y="11" width="18" height="10" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            비밀번호 변경하기
          </span>
          
          <svg v-if="showPasswordForm" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--text-muted);">
            <polyline points="18 15 12 9 6 15"></polyline>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: var(--text-muted);">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>

        <form v-if="showPasswordForm" @submit.prevent="changePassword" class="password-form">
          <div class="form-group">
            <label>현재 비밀번호</label>
            <input type="password" v-model="pwdForm.old_password" required placeholder="현재 비밀번호 입력">
          </div>
          <div class="form-group">
            <label>새 비밀번호</label>
            <input type="password" v-model="pwdForm.new_password1" required placeholder="새 비밀번호">
          </div>
          <div class="form-group">
            <label>새 비밀번호 확인</label>
            <input type="password" v-model="pwdForm.new_password2" required placeholder="새 비밀번호 확인">
          </div>
          <button type="submit" class="action-btn change-pwd-btn">비밀번호 변경</button>
        </form>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' // computed 추가
import axios from 'axios'
import { useRouter } from 'vue-router' // router 추가
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const router = useRouter()
const showPasswordForm = ref(false)

const userInfo = ref({
  nickname: '',
  age: 0,
  gender: '',
  job: '',
  income_source: '',
  mbti: '', 
  is_mydata_agreed: false
})

const pwdForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

// ★ MBTI 변환 사전
const mbtiMap = {
  safe: '성실한 개미 (안정형)',
  neutral: '신중한 햄스터 (중립형)',
  active: '똑똑한 여우 (성장형)',
  aggressive: '용감한 사자 (공격형)'
}

// ★ 화면 표시용 라벨 계산
const mbtiLabel = computed(() => {
  if (userInfo.value.mbti && mbtiMap[userInfo.value.mbti]) {
    return mbtiMap[userInfo.value.mbti]
  }
  return ''
})

// ★ 테스트 페이지 이동 함수
const goTest = () => {
  // 이미 결과가 있는데 다시 하는 경우 확인창 띄움
  if (userInfo.value.mbti) {
    if (confirm('기존 결과가 사라질 수 있습니다. 다시 테스트하시겠습니까?')) {
      router.push({ name: 'test' })
    }
  } else {
    // 결과 없으면 바로 이동
    router.push({ name: 'test' })
  }
}

// 정보 가져오기
const fetchUserInfo = async () => {
  try {
    const res = await axios.get(`${store.API_URL}/api/v1/accounts/user/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
    userInfo.value = res.data
  } catch (error) {
    console.error('정보 로딩 실패', error)
  }
}

// 정보 수정
const updateProfile = async () => {
  try {
    await axios.patch(`${store.API_URL}/api/v1/accounts/user/`, userInfo.value, {
      headers: { Authorization: `Token ${store.token}` }
    })
    alert('정보가 수정되었습니다!')
    if(userInfo.value.nickname) store.nickname = userInfo.value.nickname 
  } catch (error) {
    console.error(error)
    alert('수정 실패')
  }
}

// 비밀번호 변경
const changePassword = async () => {
  if (pwdForm.value.new_password1 !== pwdForm.value.new_password2) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }
  try {
    await axios.post(`${store.API_URL}/api/v1/accounts/password/change/`, pwdForm.value, {
      headers: { Authorization: `Token ${store.token}` }
    })
    alert('비밀번호가 변경되었습니다. 다시 로그인해주세요.')
    store.logOut()
  } catch (error) {
    console.error(error)
    alert('비밀번호 변경 실패')
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
/* =====================
  1. 전체 레이아웃 및 카드
===================== */
.mypage-container { 
  display: flex; 
  justify-content: center; 
  align-items: center; 
  min-height: 90vh; 
  background-color: var(--bg-body); /* #f5f7fa -> 변수 */
  padding: 20px; 
  transition: background-color 0.3s ease;
}

.mypage-card { 
  background: var(--bg-card); /* white -> 변수 */
  padding: 40px; 
  border-radius: 16px; 
  box-shadow: 0 4px 20px var(--shadow-color); 
  width: 100%; 
  max-width: 500px; 
  border: 1px solid var(--border-color);
}

h1 { text-align: center; margin-bottom: 5px; color: var(--text-primary); } /* #1f2937 -> 변수 */

.subtitle { 
  text-align: center; 
  color: var(--text-muted); /* #6b7280 -> 변수 */
  margin-bottom: 30px; 
  font-size: 0.9rem; 
}

.section-title { 
  font-size: 1.1rem; 
  color: var(--text-primary); /* #111827 -> 변수 */
  margin-bottom: 15px; 
  font-weight: 700; 
  border-left: 4px solid #3b82f6; 
  padding-left: 10px; 
}

/* =====================
  2. 폼 요소 (Input, Select)
===================== */
.form-group { margin-bottom: 15px; }

.form-group label { 
  display: block; 
  margin-bottom: 5px; 
  font-weight: 600; 
  color: var(--text-secondary); /* #374151 -> 변수 */
  font-size: 0.9rem; 
}

.form-group input, .form-group select { 
  width: 100%; 
  padding: 10px; 
  border: 1px solid var(--border-color); /* #d1d5db -> 변수 */
  border-radius: 6px; 
  font-size: 0.95rem; 
  box-sizing: border-box; 
  background-color: var(--bg-card); /* 라이트 모드에서도 변수 사용 권장 */
  color: var(--text-primary);
  transition: border-color 0.2s;
}

.form-group input:focus { border-color: #3b82f6; outline: none; }

/* =====================
  3. MBTI 표시 영역 (가시성 조정)
===================== */
.mbti-display {
  display: flex; 
  align-items: center; 
  justify-content: space-between;
  padding: 8px 10px; 
  background-color: var(--bg-body); /* 카드 내부 박스는 전체 배경색과 통일하여 깊이감 부여 */
  border: 1px solid var(--border-color);
  border-radius: 6px; 
  height: 45px; 
  box-sizing: border-box;
}

.mbti-result { font-weight: 700; color: #3b82f6; font-size: 0.95rem; }
.mbti-none { color: var(--text-muted); font-size: 0.9rem; }

/* 버튼 스타일 (Retest / Start) */
.retest-btn, .start-test-btn {
  background: var(--bg-card); 
  border: 1px solid var(--border-color); 
  padding: 4px 10px;
  border-radius: 4px; 
  font-size: 0.8rem; 
  cursor: pointer; 
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.2s; 
  white-space: nowrap;
}

.retest-btn:hover { background: var(--bg-hover); color: #3b82f6; border-color: #3b82f6; }

.start-test-btn { 
  background: var(--bg-badge); /* 라이트: 밝은블루, 다크: 짙은회색 */
  color: #3182f6; 
  border-color: rgba(59, 130, 246, 0.3); 
}
.start-test-btn:hover { background: #3b82f6; color: white; border-color: #3b82f6; }

/* =====================
  4. 기타 요소 및 비밀번호 폼
==================== */
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }

.agreement-box { 
  background-color: var(--bg-body); 
  padding: 12px; 
  border-radius: 6px; 
  display: flex; 
  gap: 10px; 
  align-items: flex-start; 
  margin: 20px 0; 
  border: 1px solid var(--border-color);
}

.agreement-box label { font-size: 0.9rem; cursor: pointer; color: var(--text-secondary); }
.agreement-box .desc { display: block; font-size: 0.8rem; color: var(--text-muted); margin-top: 2px; }

.action-btn { width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: background 0.2s; }
.update-btn { background-color: #3b82f6; color: white; }
.update-btn:hover { background-color: #2563eb; }

.divider { margin: 30px 0; border: none; border-top: 1px solid var(--border-color); }

.toggle-btn { 
  background: none; 
  border: none; 
  color: var(--text-secondary); 
  font-weight: 600; 
  cursor: pointer; 
  width: 100%; 
  text-align: left; 
  padding: 0; 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
}

.password-form { 
  margin-top: 20px; 
  background-color: var(--bg-body); 
  padding: 20px; 
  border-radius: 8px; 
  border: 1px solid var(--border-color); 
}

.change-pwd-btn { background-color: #4b5563; color: white; margin-top: 10px; }
.change-pwd-btn:hover { background-color: #374151; }
/* Chrome, Safari, Edge, Opera */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* 아이콘 SVG 공통 스타일 */
.icon-svg {
  vertical-align: text-bottom; /* 텍스트와 높이 맞춤 */
  margin-right: 4px;           /* 텍스트와의 간격 */
  color: inherit;              /* 부모 요소 색상 상속 */
}

/* 섹션 타이틀 아이콘 정렬 */
.section-title {
  display: flex;
  align-items: center;
  gap: 6px; /* 아이콘과 타이틀 간격 */
}

/* 비밀번호 토글 버튼 내부 정렬 보완 */
.toggle-btn {
  /* 기존 코드에 display: flex; 가 있어서 잘 정렬되지만 확실하게 하기 위함 */
  align-items: center; 
}
</style>