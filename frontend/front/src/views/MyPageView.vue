<template>
  <div class="mypage-container">
    <div class="mypage-card">
      <h1>마이페이지</h1>
      <p class="subtitle">내 정보를 확인하고 수정할 수 있습니다.</p>

      <form @submit.prevent="updateProfile">
        <h3 class="section-title">👤 내 정보 수정</h3>

        <div class="form-group">
          <label>닉네임</label>
          <input type="text" v-model="userInfo.nickname">
        </div>

        <div class="row">
          <div class="form-group">
            <label>나이</label>
            <input type="number" v-model.number="userInfo.age">
          </div>
          <div class="form-group">
            <label>자산 (만원)</label>
            <input type="number" v-model.number="userInfo.wealth">
          </div>
        </div>
        
        <div class="form-group">
            <label>연봉 (만원)</label>
            <input type="number" v-model.number="userInfo.salary">
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth' // ★ 여기를 본인 스토어 파일명에 맞게 수정 (auth 또는 counter)

const store = useAuthStore()
const showPasswordForm = ref(false)

const userInfo = ref({
  nickname: '',
  age: 0,
  wealth: 0,
  salary: 0,
  is_mydata_agreed: false
})

const pwdForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})

// 정보 가져오기
const fetchUserInfo = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/v1/accounts/user/', {
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
    await axios.patch('http://127.0.0.1:8000/api/v1/accounts/user/', userInfo.value, {
      headers: { Authorization: `Token ${store.token}` }
    })
    alert('정보가 수정되었습니다!')
    // 닉네임 즉시 반영
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
    await axios.post('http://127.0.0.1:8000/api/v1/accounts/password/change/', pwdForm.value, {
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
.mypage-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 90vh;
  background-color: #f5f7fa;
  padding: 20px;
}
.mypage-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 500px;
}
h1 { text-align: center; margin-bottom: 5px; color: #1f2937; }
.subtitle { text-align: center; color: #6b7280; margin-bottom: 30px; font-size: 0.9rem; }
.section-title { font-size: 1.1rem; color: #111827; margin-bottom: 15px; font-weight: 700; border-left: 4px solid #3b82f6; padding-left: 10px; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #374151; font-size: 0.9rem; }
.form-group input { 
  width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; 
  font-size: 0.95rem; box-sizing: border-box;
}
.row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.agreement-box { 
  background-color: #f3f4f6; padding: 12px; border-radius: 6px; 
  display: flex; gap: 10px; align-items: flex-start; margin: 20px 0;
}
.agreement-box input { width: 18px; height: 18px; margin-top: 2px; flex-shrink: 0; }
.agreement-box label { font-size: 0.9rem; cursor: pointer; }
.agreement-box .desc { display: block; font-size: 0.8rem; color: #6b7280; margin-top: 2px; }
.action-btn {
  width: 100%; padding: 12px; border: none; border-radius: 8px; 
  font-size: 1rem; font-weight: 700; cursor: pointer; transition: background 0.2s;
}
.update-btn { background-color: #3b82f6; color: white; }
.update-btn:hover { background-color: #2563eb; }
.divider { margin: 30px 0; border: none; border-top: 1px solid #e5e7eb; }
.toggle-btn {
  background: none; border: none; color: #4b5563; font-weight: 600; 
  cursor: pointer; width: 100%; text-align: left; padding: 0;
  display: flex; justify-content: space-between; align-items: center;
}
.password-form { margin-top: 20px; background-color: #f9fafb; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; }
.change-pwd-btn { background-color: #4b5563; color: white; margin-top: 10px; }
.change-pwd-btn:hover { background-color: #374151; }
</style>