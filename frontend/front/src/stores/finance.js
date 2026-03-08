import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', () => {
  const products = ref([])
  const savingProducts = ref([])
  const exchangeRates = ref([])
  const joinedProducts = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getProducts = function () {
    axios.get(`${API_URL}/api/v1/products/deposit-products/`)
      .then(res => { products.value = res.data })
  }

  const getSavingProducts = function () {
    axios.get(`${API_URL}/api/v1/products/saving-products/`)
      .then(res => { savingProducts.value = res.data })
  }

  const getExchangeRates = function () {
    axios.get(`${API_URL}/api/v1/exchange/exchange-rates/`) 
      .then(res => { exchangeRates.value = res.data })
  }

  const joinProduct = (product) => {
    const exists = joinedProducts.value.some(p => p.fin_prdt_cd === product.fin_prdt_cd)
    if (exists) { alert('이미 가입한 상품입니다.'); return }
    joinedProducts.value.push(product)
    alert('가입 리스트에 추가되었습니다!')
  }

  const cancelProduct = (productId) => {
    const index = joinedProducts.value.findIndex(p => p.fin_prdt_cd === productId)
    if (index !== -1) {
      joinedProducts.value.splice(index, 1)
    }
  }

  const isJoined = (productId) => {
    return joinedProducts.value.some(p => p.fin_prdt_cd === productId)
  }

  return { 
    products, savingProducts, exchangeRates, joinedProducts,
    getProducts, getSavingProducts, getExchangeRates,
    joinProduct, cancelProduct, isJoined
  }
}, { persist: true })