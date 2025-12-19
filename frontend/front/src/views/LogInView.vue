<template>
  <div class="auth-container">
    <h1>로그인</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="username">아이디: </label>
        <input type="text" id="username" v-model.trim="username">
      </div>
      <div>
        <label for="password">비밀번호: </label>
        <input type="password" id="password" v-model.trim="password">
      </div>
      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()
const username = ref(null)
const password = ref(null)

const submitForm = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}
</script>

<style scoped>
.auth-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}
input {
  margin: 10px;
  padding: 8px;
}
</style>