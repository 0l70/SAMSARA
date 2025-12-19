import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useCounterStore = defineStore('counter', () => {
  const products = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getProducts = function () {
    axios.get(`${API_URL}/api/v1/products/deposit-products/`)
      .then((res) => {
        console.log('데이터 가져오기 성공!', res.data)
        products.value = res.data
      })
      .catch((err) => console.log(err))
  }

  return { products, getProducts }
})