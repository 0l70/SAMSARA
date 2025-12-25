import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  // --------------------------------------------------
  // 1. 상태 변수 (State)
  // --------------------------------------------------
  // 뷰 파일에서 'store.products'라고 부르므로 이름을 products로 통일
  const products = ref([])         // 예금 상품 리스트
  const savingProducts = ref([])   // 적금 상품 리스트
  const exchangeRates = ref([])    // 환율 데이터
  const joinedProducts = ref([])   // 가입한 상품 리스트
  
  const API_URL = 'http://127.0.0.1:8000'

  // --------------------------------------------------
  // 2. API 액션 (Actions)
  // --------------------------------------------------
  
  // (1) 예금 가져오기 (이름 변경: getDepositProducts -> getProducts)
  const getProducts = function () {
    axios.get(`${API_URL}/api/v1/products/deposit-products/`)
      .then(res => {
        products.value = res.data
        console.log('예금 데이터 로드 완료')
      })
      .catch(err => console.log('예금 로드 실패:', err))
  }

  // (2) 적금 가져오기
  const getSavingProducts = function () {
    axios.get(`${API_URL}/api/v1/products/saving-products/`)
      .then(res => {
        savingProducts.value = res.data
        console.log('적금 데이터 로드 완료')
      })
      .catch(err => console.log('적금 로드 실패:', err))
  }

  // (3) 환율 데이터 가져오기
  const getExchangeRates = function () {
    axios.get(`${API_URL}/api/v1/exchange/exchange-rates/`) 
      .then(res => {
        exchangeRates.value = res.data
        console.log('환율 데이터 로드 완료')
      })
      .catch(err => console.log(err))
  }

  // --------------------------------------------------
  // 3. 가입/해지 기능
  // --------------------------------------------------
  const joinProduct = (product) => {
    // 중복 가입 방지
    const exists = joinedProducts.value.some(p => p.fin_prdt_cd === product.fin_prdt_cd)
    if (exists) {
      alert('이미 가입한 상품입니다. 😅')
      return
    }
    joinedProducts.value.push(product)
    alert('가입 리스트에 추가되었습니다! 🎉')
  }

  const cancelProduct = (productId) => {
    const index = joinedProducts.value.findIndex(p => p.fin_prdt_cd === productId)
    if (index !== -1) {
      if (confirm('정말 이 상품을 해지하시겠습니까?')) {
        joinedProducts.value.splice(index, 1)
        alert('상품이 해지되었습니다.')
      }
    }
  }

  const isJoined = (productId) => {
    return joinedProducts.value.some(p => p.fin_prdt_cd === productId)
  }

  return { 
    // State (변수명 products로 내보냄)
    products, 
    savingProducts, 
    exchangeRates,
    joinedProducts,
    
    // Actions (함수명 getProducts로 내보냄)
    getProducts, 
    getSavingProducts, 
    getExchangeRates,
    joinProduct,
    cancelProduct,
    isJoined
  }
}, { persist: true })