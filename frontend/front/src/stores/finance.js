import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const products = ref([])         // 예금 리스트
  const savingProducts = ref([])   // ▼ 적금 리스트 추가
  const API_URL = 'http://127.0.0.1:8000'
  const exchangeRates = ref([]) // ▼ 환율 데이터 저장소

  // 예금 가져오기
  const getProducts = function () {
    axios.get(`${API_URL}/api/v1/products/deposit-products/`)
      .then(res => products.value = res.data)
      .catch(err => console.log(err))
  }

  // ▼ 적금 가져오기 함수 추가
  const getSavingProducts = function () {
    axios.get(`${API_URL}/api/v1/products/saving-products/`)
      .then(res => savingProducts.value = res.data)
      .catch(err => console.log(err))
  }
// ▼ 환율 데이터 가져오기
  const getExchangeRates = function () {
    axios.get(`${API_URL}/api/v1/exchange/`)
      .then(res => {
        exchangeRates.value = res.data
        console.log('환율 데이터 로드 완료')
      })
      .catch(err => console.log(err))
  }

  return { 
    products, savingProducts, exchangeRates, // export 추가
    getProducts, getSavingProducts, getExchangeRates 
  }
})