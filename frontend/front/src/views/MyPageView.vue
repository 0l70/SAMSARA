<template>
  <div class="mypage-container">
    <div class="mypage-card">
      <h1>마이페이지</h1>
      <p class="subtitle">내 정보를 확인하고 수정할 수 있습니다.</p>

      <form @submit.prevent="updateProfile">
        <h3 class="section-title">👤 내 정보 수정</h3>

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
          🔒 비밀번호 변경하기 {{ showPasswordForm ? '▲' : '▼' }}
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
.mypage-container { display: flex; justify-content: center; align-items: center; min-height: 90vh; background-color: #f5f7fa; padding: 20px; }
.mypage-card { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 500px; }
h1 { text-align: center; margin-bottom: 5px; color: #1f2937; }
.subtitle { text-align: center; color: #6b7280; margin-bottom: 30px; font-size: 0.9rem; }
.section-title { font-size: 1.1rem; color: #111827; margin-bottom: 15px; font-weight: 700; border-left: 4px solid #3b82f6; padding-left: 10px; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #374151; font-size: 0.9rem; }

/* input과 select 스타일 통일 */
.form-group input, .form-group select { 
  width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; 
  font-size: 0.95rem; box-sizing: border-box; background-color: white;
}

/* ★ MBTI 표시 영역 스타일 (input과 유사하게 만듦) */
.mbti-display {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 10px; background-color: #f9fafb; border: 1px solid #d1d5db;
  border-radius: 6px; height: 45px; box-sizing: border-box;
}
.mbti-result { font-weight: 700; color: #3b82f6; font-size: 0.95rem; }
.mbti-none { color: #9ca3af; font-size: 0.9rem; }

/* 버튼 스타일 */
.retest-btn, .start-test-btn {
  background: white; border: 1px solid #d1d5db; padding: 4px 10px;
  border-radius: 4px; font-size: 0.8rem; cursor: pointer; font-weight: 600;
  transition: all 0.2s; white-space: nowrap;
}
.retest-btn:hover { background: #f3f4f6; color: #3b82f6; border-color: #3b82f6; }
.start-test-btn { background: #eff6ff; color: #3b82f6; border-color: #bfdbfe; }
.start-test-btn:hover { background: #3b82f6; color: white; border-color: #3b82f6; }

.row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.agreement-box { background-color: #f3f4f6; padding: 12px; border-radius: 6px; display: flex; gap: 10px; align-items: flex-start; margin: 20px 0; }
.agreement-box input { width: 18px; height: 18px; margin-top: 2px; flex-shrink: 0; }
.agreement-box label { font-size: 0.9rem; cursor: pointer; }
.agreement-box .desc { display: block; font-size: 0.8rem; color: #6b7280; margin-top: 2px; }
.action-btn { width: 100%; padding: 12px; border: none; border-radius: 8px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: background 0.2s; }
.update-btn { background-color: #3b82f6; color: white; }
.update-btn:hover { background-color: #2563eb; }
.divider { margin: 30px 0; border: none; border-top: 1px solid #e5e7eb; }
.toggle-btn { background: none; border: none; color: #4b5563; font-weight: 600; cursor: pointer; width: 100%; text-align: left; padding: 0; display: flex; justify-content: space-between; align-items: center; }
.password-form { margin-top: 20px; background-color: #f9fafb; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; }
.change-pwd-btn { background-color: #4b5563; color: white; margin-top: 10px; }
.change-pwd-btn:hover { background-color: #374151; }
</style>