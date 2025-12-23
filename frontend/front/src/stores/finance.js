import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  // --------------------------------------------------
  // 1. 상태 변수 (State)
  // --------------------------------------------------
  const products = ref([])        // 예금 상품 리스트
  const savingProducts = ref([])  // 적금 상품 리스트
  const exchangeRates = ref([])   // 환율 데이터
  const joinedProducts = ref([])  // 📌 가입한 상품 리스트 (장바구니 개념)
  
  const API_URL = 'http://127.0.0.1:8000'

  // --------------------------------------------------
  // 2. API 액션 (Actions - Fetch Data)
  // --------------------------------------------------
  
  // (1) 예금 가져오기
  const getProducts = function () {
    axios.get(`${API_URL}/api/v1/products/deposit-products/`)
      .then(res => products.value = res.data)
      .catch(err => console.log(err))
  }

  // (2) 적금 가져오기
  const getSavingProducts = function () {
    axios.get(`${API_URL}/api/v1/products/saving-products/`)
      .then(res => savingProducts.value = res.data)
      .catch(err => console.log(err))
  }

  // (3) 환율 데이터 가져오기
  const getExchangeRates = function () {
    // API 주소가 뷰에서 쓰는 것과 맞는지 꼭 확인하세요! (보통 끝에 /exchange-rates/ 등)
    axios.get(`${API_URL}/api/v1/exchange/exchange-rates/`) 
      .then(res => {
        exchangeRates.value = res.data
        console.log('환율 데이터 로드 완료')
      })
      .catch(err => console.log(err))
  }

  // --------------------------------------------------
  // 3. 가입/해지 액션 (Actions - User Interaction)
  // --------------------------------------------------

  // (1) 가입하기 (중복 체크 포함)
  const joinProduct = (product) => {
    // 이미 가입된 상품인지 ID(fin_prdt_cd)로 확인
    const exists = joinedProducts.value.some(p => p.fin_prdt_cd === product.fin_prdt_cd)
    
    if (exists) {
      alert('이미 가입한 상품입니다. 😅')
      return
    }
    
    // 리스트에 추가
    joinedProducts.value.push(product)
    alert('가입 리스트에 추가되었습니다! 🎉')
  }

  // (2) 해지하기 (삭제)
  const cancelProduct = (productId) => {
    // 삭제할 인덱스 찾기
    const index = joinedProducts.value.findIndex(p => p.fin_prdt_cd === productId)
    
    if (index !== -1) {
      const confirmCancel = confirm('정말 이 상품을 해지하시겠습니까?')
      if (confirmCancel) {
        joinedProducts.value.splice(index, 1) // 배열에서 제거
        alert('상품이 해지되었습니다.')
      }
    }
  }

  // (3) 가입 여부 확인 (버튼 UI용)
  const isJoined = (productId) => {
    return joinedProducts.value.some(p => p.fin_prdt_cd === productId)
  }

  return { 
    // State
    products, 
    savingProducts, 
    exchangeRates,
    joinedProducts,
    
    // Actions
    getProducts, 
    getSavingProducts, 
    getExchangeRates,
    joinProduct,
    cancelProduct,
    isJoined
  }
}, { persist: true }) // 📌 중요: 새로고침 해도 가입 목록 유지