<template>
  <div class="page-container">
    <div class="content-wrapper">
      
      <div class="header-section">
        <div class="title-area">
          <span class="sub-badge">MAP SERVICE</span>
          <h1>주변 은행 찾기</h1>
        </div>
        <p class="desc">지역과 은행을 선택해 가까운 지점을 찾아보세요.</p>
      </div>

      <section class="filter-card">
        <div class="filter-top">
          <div class="select-group">
            <select v-model="selectedCity" @change="onCityChange">
              <option value="">시/도 선택</option>
              <option v-for="c in data.mapInfo" :key="c.name" :value="c.name">
                {{ c.name }}
              </option>
            </select>

            <select v-model="selectedCountry">
              <option value="">구/군 선택</option>
              <option v-for="c in countries" :key="c">{{ c }}</option>
            </select>
          </div>

          <button class="search-btn" @click="searchByMultipleBanks">
            검색하기
          </button>
        </div>

        <div class="divider"></div>

        <div class="banks-group">
          <div class="banks-label">은행 선택</div>
          <div class="banks-grid">
            <button
              v-for="bank in data.bankInfo"
              :key="bank"
              class="bank-chip"
              :class="{ active: selectedBanks.includes(bank) }"
              @click="toggleBank(bank)"
            >
              {{ bank }}
            </button>
          </div>
        </div>
      </section>

      <main class="content-grid">
        <div class="map-wrapper">
          <div id="map" class="map"></div>
          
          <button class="loc-btn" @click="findMyLocation(true)" title="내 위치 찾기">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4b5563" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="22" y1="12" x2="18" y2="12"></line>
              <line x1="6" y1="12" x2="2" y2="12"></line>
              <line x1="12" y1="6" x2="12" y2="2"></line>
              <line x1="12" y1="22" x2="12" y2="18"></line>
            </svg>
          </button>
        </div>

        <aside class="list-wrapper">
          <div class="list-header">
            <h3>검색 결과 <span class="count">{{ places.length }}</span></h3>
            <span v-if="isLoading" class="loading-text">· 검색중...</span>
          </div>

          <div v-if="!places.length && !isLoading" class="empty-state">
            <div class="empty-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </div>
            <p>조건을 선택하고 검색해주세요</p>
          </div>

          <ul v-else class="place-list">
            <li
              v-for="(p, i) in places"
              :key="p.id"
              class="place-item"
              @click="selectPlace(p)"
            >
              <div class="place-info">
                <div class="place-title">
                  <span class="idx">{{ i + 1 }}</span>
                  {{ p.place_name }}
                </div>
                <div class="place-addr">{{ p.address_name }}</div>
                <div v-if="p.phone" class="place-phone">{{ p.phone }}</div>
              </div>

              <div class="place-action">
                <button class="route-btn" @click.stop="drawRouteTo(p)">
                  길찾기 ➔
                </button>
              </div>
            </li>
          </ul>
        </aside>
      </main>

    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios' // ⚡ API 호출용 (npm install axios 필요)

/* =========================================================
   1. 데이터 및 변수 선언
   ========================================================= */
const KAKAO_JS_KEY = import.meta.env.VITE_KAKAO_JS_KEY
const KAKAO_REST_KEY = import.meta.env.VITE_KAKAO_REST_KEY

/* 데이터 (기존 동일) */
const data = {

    "mapInfo": [

      {

        "name": "서울특별시",

        "countries": [

          "강남구",

          "강동구",

          "강북구",

          "강서구",

          "관악구",

          "광진구",

          "구로구",

          "금천구",

          "노원구",

          "도봉구",

          "동대문구",

          "동작구",

          "마포구",

          "서대문구",

          "서초구",

          "성동구",

          "성북구",

          "송파구",

          "양천구",

          "영등포구",

          "용산구",

          "은평구",

          "종로구",

          "중구",

          "중랑구"

        ]

      },

      {

        "name": "부산광역시",

        "countries": [

          "강서구",

          "금정구",

          "기장군",

          "남구",

          "동구",

          "동래구",

          "부산진구",

          "북구",

          "사상구",

          "사하구",

          "서구",

          "수영구",

          "연제구",

          "영도구",

          "중구",

          "해운대구"

        ]

      },

      {

        "name": "대구광역시",

        "countries": [

          "남구",

          "달서구",

          "달성군",

          "동구",

          "북구",

          "서구",

          "수성구",

          "중구"

        ]

      },

      {

        "name": "인천광역시",

        "countries": [

          "강화군",

          "계양구",

          "남구",

          "남동구",

          "동구",

          "부평구",

          "서구",

          "연수구",

          "옹진군",

          "중구"

        ]

      },

      {

        "name": "광주광역시",

        "countries": ["광산구", "남구", "동구", "북구", "서구"]

      },

      {

        "name": "대전광역시",

        "countries": ["대덕구", "동구", "서구", "유성구", "중구"]

      },

      {

        "name": "울산광역시",

        "countries": ["남구", "동구", "북구", "울주군", "중구"]

      },

      {

        "name": "경기도",

        "countries": [

          "가평군",

          "고양시 덕양구",

          "고양시 일산동구",

          "고양시 일산서구",

          "과천시",

          "광명시",

          "광주시",

          "구리시",

          "군포시",

          "김포시",

          "남양주시",

          "동두천시",

          "부천시 소사구",

          "부천시 오정구",

          "부천시 원미구",

          "성남시 분당구",

          "성남시 수정구",

          "성남시 중원구",

          "수원시 권선구",

          "수원시 영통구",

          "수원시 장안구",

          "수원시 팔달구",

          "시흥시",

          "안산시 단원구",

          "안산시 상록구",

          "안성시",

          "안양시 동안구",

          "안양시 만안구",

          "양주시",

          "양평군",

          "여주군",

          "연천군",

          "오산시",

          "용인시 기흥구",

          "용인시 수지구",

          "용인시 처인구",

          "의왕시",

          "의정부시",

          "이천시",

          "파주시",

          "평택시",

          "포천시",

          "하남시",

          "화성시"

        ]

      },

      {

        "name": "강원도",

        "countries": [

          "강릉시",

          "고성군",

          "동해시",

          "삼척시",

          "속초시",

          "양구군",

          "양양군",

          "영월군",

          "원주시",

          "인제군",

          "정선군",

          "철원군",

          "춘천시",

          "태백시",

          "평창군",

          "홍천군",

          "화천군",

          "횡성군"

        ]

      },

      {

        "name": "충청북도",

        "countries": [

          "괴산군",

          "단양군",

          "보은군",

          "영동군",

          "옥천군",

          "음성군",

          "제천시",

          "증평군",

          "진천군",

          "청원군",

          "청주시 상당구",

          "청주시 흥덕구",

          "충주시"

        ]

      },

      {

        "name": "충청남도",

        "countries": [

          "계룡시",

          "공주시",

          "금산군",

          "논산시",

          "당진시",

          "보령시",

          "부여군",

          "서산시",

          "서천군",

          "아산시",

          "연기군",

          "예산군",

          "천안시 동남구",

          "천안시 서북구",

          "청양군",

          "태안군",

          "홍성군"

        ]

      },

      {

        "name": "전라북도",

        "countries": [

          "고창군",

          "군산시",

          "김제시",

          "남원시",

          "무주군",

          "부안군",

          "순창군",

          "완주군",

          "익산시",

          "임실군",

          "장수군",

          "전주시 덕진구",

          "전주시 완산구",

          "정읍시",

          "진안군"

        ]

      },

      {

        "name": "전라남도",

        "countries": [

          "강진군",

          "고흥군",

          "곡성군",

          "광양시",

          "구례군",

          "나주시",

          "담양군",

          "목포시",

          "무안군",

          "보성군",

          "순천시",

          "신안군",

          "여수시",

          "영광군",

          "영암군",

          "완도군",

          "장성군",

          "장흥군",

          "진도군",

          "함평군",

          "해남군",

          "화순군"

        ]

      },

      {

        "name": "경상북도",

        "countries": [

          "경산시",

          "경주시",

          "고령군",

          "구미시",

          "군위군",

          "김천시",

          "문경시",

          "봉화군",

          "상주시",

          "성주군",

          "안동시",

          "영덕군",

          "영양군",

          "영주시",

          "영천시",

          "예천군",

          "울릉군",

          "울진군",

          "의성군",

          "청도군",

          "청송군",

          "칠곡군",

          "포항시 남구",

          "포항시 북구"

        ]

      },

      {

        "name": "경상남도",

        "countries": [

          "거제시",

          "거창군",

          "고성군",

          "김해시",

          "남해군",

          "밀양시",

          "사천시",

          "산청군",

          "양산시",

          "의령군",

          "진주시",

          "창녕군",

          "창원시 마산합포구",

          "창원시 마산회원구",

          "창원시 성산구",

          "창원시 의창구",

          "창원시 진해구",

          "통영시",

          "하동군",

          "함안군",

          "함양군",

          "합천군"

        ]

      },

      {

        "name": "제주도",

        "countries": ["서귀포시", "제주시"]

      },

      {

        "name": "세종시",

        "countries": ["세종시"]

      }

    ],

    "bankInfo": [

      "국민은행",

      "신한은행",

      "우리은행",

      "하나은행",

      "산업은행",

      "새마을금고",

      "우체국",
      
      "농협",
      
      "신협",

      "기업은행",

      "부산은행",

      "대구은행",

      "광주은행",

      "경남은행",

      "전북은행",

      "제주은행",

      "수협"

    ]

  }

// 은행 버튼 2줄로 나누기
const half = Math.ceil(data.bankInfo.length / 2)
const row1 = data.bankInfo.slice(0, half)
const row2 = data.bankInfo.slice(half)

// 반응형 상태 변수들
const map = ref(null)
const places = ref([])       // 검색된 은행 목록
const markers = ref([])      // 지도 위 마커들
const infowindow = ref(null)
const myLat = ref(null)      // 내 위치 위도
const myLon = ref(null)      // 내 위치 경도
const myMarker = ref(null)   // 내 위치 마커
const polyline = ref(null)   // 경로 선
const isLoading = ref(false) // 로딩 중 표시

// 필터 선택 값
const selectedCity = ref('')
const selectedCountry = ref('')
const selectedBanks = ref([])
const countries = ref([])    // 선택된 시/도에 따른 구/군 목록


/* =========================================================
  2. 초기화 (onMounted)
   ========================================================= */
onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    initMap()
  } else {
    const script = document.createElement('script')
    // ❗ 본인의 JS 키로 교체 필요
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_JS_KEY}&libraries=services`
    document.head.appendChild(script)
    script.onload = () => window.kakao.maps.load(initMap)
  }
})

const initMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new window.kakao.maps.LatLng(37.566826, 126.9786567),
    level: 3
  }
  map.value = new window.kakao.maps.Map(container, options)
  infowindow.value = new window.kakao.maps.InfoWindow({ zIndex: 1 })

  // 시작하자마자 내 위치 찾기
  findMyLocation(false)
}


/* =========================================================
  3. 검색 및 필터 로직
   ========================================================= */
// 시/도 변경 시 구/군 목록 업데이트 (🚨 질문하신 부분 해결!)
const onCityChange = () => {
  const city = data.mapInfo.find((c) => c.name === selectedCity.value)
  countries.value = city ? city.countries : []
  selectedCountry.value = '' // 구/군 초기화
}

// 은행 다중 선택 토글
const toggleBank = (bank) => {
  if (selectedBanks.value.includes(bank)) {
    selectedBanks.value = selectedBanks.value.filter(b => b !== bank)
  } else {
    selectedBanks.value.push(bank)
  }
}

// 검색 실행
const searchByMultipleBanks = async () => {
  if (!selectedCity.value || !selectedCountry.value) {
    alert('시/도와 구/군을 먼저 선택해주세요.')
    return
  }
  if (selectedBanks.value.length === 0) {
    alert('은행을 최소 1개 이상 선택해주세요.')
    return
  }

  isLoading.value = true
  places.value = []
  removeAllMarkers()
  if (polyline.value) polyline.value.setMap(null)

  const ps = new window.kakao.maps.services.Places()
  const searchPromises = []

  // 선택한 은행별로 검색 요청 병렬 처리
  selectedBanks.value.forEach(bank => {
    const keyword = `${selectedCity.value} ${selectedCountry.value} ${bank}`
    const p = new Promise((resolve) => {
      ps.keywordSearch(keyword, (data, status) => {
        resolve(status === window.kakao.maps.services.Status.OK ? data : [])
      })
    })
    searchPromises.push(p)
  })

  try {
    const results = await Promise.all(searchPromises)
    // 결과 합치기 및 중복 제거
    const merged = results.flat()
    const uniqueMap = new Map()
    merged.forEach(item => uniqueMap.set(item.id, item))
    const uniquePlaces = Array.from(uniqueMap.values())

    places.value = uniquePlaces
    
    if (uniquePlaces.length > 0) {
      displayPlaces(uniquePlaces)
      setBounds(uniquePlaces)
    } else {
      alert("검색 결과가 없습니다.")
    }
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

// 검색 결과 마커 표시
const displayPlaces = (data) => {
  data.forEach((place) => {
    const marker = new window.kakao.maps.Marker({
      map: map.value,
      position: new window.kakao.maps.LatLng(place.y, place.x)
    })
    window.kakao.maps.event.addListener(marker, 'click', () => {
      selectPlace(place)
    })
    markers.value.push(marker)
  })
}

const removeAllMarkers = () => {
  markers.value.forEach(m => m.setMap(null))
  markers.value = []
}

const setBounds = (data) => {
  const bounds = new window.kakao.maps.LatLngBounds()
  data.forEach(place => bounds.extend(new window.kakao.maps.LatLng(place.y, place.x)))
  map.value.setBounds(bounds)
}


/* =========================================================
  4. 위치 및 경로(Route) 로직
   ========================================================= */
// 내 위치 찾기
const findMyLocation = (moveMap = true) => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      myLat.value = position.coords.latitude
      myLon.value = position.coords.longitude
      const locPosition = new window.kakao.maps.LatLng(myLat.value, myLon.value)

      if (myMarker.value) myMarker.value.setMap(null)

      // 빨간색 핀 이미지
      const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png'
      const imageSize = new window.kakao.maps.Size(64, 69)
      const imageOption = { offset: new window.kakao.maps.Point(27, 69) }
      const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imageOption)

      myMarker.value = new window.kakao.maps.Marker({
        map: map.value,
        position: locPosition,
        image: markerImage
      })

      if (moveMap) map.value.setCenter(locPosition)
    })
  } else {
    alert("위치 정보를 사용할 수 없습니다.")
  }
}

// 리스트 클릭 시 지도 이동 및 경로 그리기
const selectPlace = (place) => {
  const pos = new window.kakao.maps.LatLng(place.y, place.x)
  map.value.panTo(pos)
  drawRouteTo(place) // 자동으로 경로 그리기 실행
}

// ⚡ [핵심] 실제 도로 경로 그리기 함수
const drawRouteTo = async (place) => {
  if (!myLat.value || !myLon.value) {
    alert("내 위치를 먼저 찾아주세요!")
    return
  }

  // 기존 선 제거
  if (polyline.value) polyline.value.setMap(null)

  const origin = `${myLon.value},${myLat.value}`
  const destination = `${place.x},${place.y}`

  try {
    // 🚨 주의: 브라우저 직접 호출 시 CORS 에러 발생 가능 (백엔드 프록시 권장)
    const res = await axios.get('https://apis-navi.kakaomobility.com/v1/directions', {
      params: { origin, destination, priority: 'RECOMMEND' },
      headers: { Authorization: `KakaoAK ${KAKAO_REST_KEY}` }
    })

    const routes = res.data.routes[0]
    const linePath = []
    
    // 경로 데이터 파싱 (Vertex -> LatLng)
    routes.sections.forEach(section => {
      section.roads.forEach(road => {
        const vertexes = road.vertexes
        for (let i = 0; i < vertexes.length; i += 2) {
          linePath.push(new window.kakao.maps.LatLng(vertexes[i+1], vertexes[i]))
        }
      })
    })

    // 선 그리기
    polyline.value = new window.kakao.maps.Polyline({
      path: linePath,
      strokeWeight: 6,
      strokeColor: '#FF3399',
      strokeOpacity: 0.8,
      strokeStyle: 'solid'
    })
    polyline.value.setMap(map.value)

    // 정보창에 거리/시간 표시
    const duration = Math.round(routes.summary.duration / 60) + '분'
    const distance = (routes.summary.distance / 1000).toFixed(1) + 'km'
    
    const content = `
      <div style="padding:10px; font-size:13px; text-align:center; background:white; border-radius:5px; border:1px solid #ccc;">
        <strong>${place.place_name}</strong><br>
        🚗 ${duration} / ${distance}
      </div>`
    
    infowindow.value.setContent(content)
    infowindow.value.open(map.value, new window.kakao.maps.Marker({
      position: new window.kakao.maps.LatLng(place.y, place.x), 
      map: null 
    }))

    // 경로가 모두 보이게 지도 범위 조정
    const bounds = new window.kakao.maps.LatLngBounds()
    linePath.forEach(p => bounds.extend(p))
    map.value.setBounds(bounds)

  } catch (err) {
    console.error("경로 요청 실패:", err)
    alert("경로를 불러오지 못했습니다 (키 확인/CORS)")
  }
}
</script>

<style scoped>
/* =====================
  1. 전체 레이아웃 (변수 적용)
===================== */
.page-container {
  /* 배경색 변수 적용 */
  background-color: var(--bg-body);
  min-height: 100vh;
  padding: 40px 20px;
  transition: background-color 0.3s ease;
}

.content-wrapper {
  max-width: 1280px;
  margin: 0 auto;
}

/* =====================
  2. 헤더 섹션
===================== */
.header-section {
  text-align: left;
  margin-bottom: 40px;
}

.sub-badge {
  display: inline-block;
  color: var(--primary-color);
  font-weight: 700;
  font-size: 14px;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.title-area h1 {
  font-size: 32px;
  font-weight: 800;
  /* 텍스트 색상 변수 적용 */
  color: var(--text-primary);
  margin: 0 0 10px 0;
  line-height: 1.3;
}

.desc {
  color: var(--text-secondary);
  font-size: 16px;
  margin: 0;
}

/* =====================
  3. 필터 카드 (다크모드 대응)
===================== */
.filter-card {
  background: var(--bg-card);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.select-group {
  display: flex;
  gap: 12px;
  flex: 1;
}

.filter-card select {
  height: 48px;
  padding: 0 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  font-size: 15px;
  color: var(--text-primary);
  min-width: 140px;
  outline: none;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-card select:focus {
  border-color: var(--primary-color);
}

.search-btn {
  height: 48px;
  padding: 0 32px;
  border-radius: 12px;
  /* 버튼은 아까 맞춘 톤다운 블루 적용 */
  background-color: #4a86e8;
  color: white;
  border: none;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 10px rgba(74, 134, 232, 0.2);
}

/* 검색 버튼 다크모드 전용 */
:global([data-theme="dark"]) .search-btn {
  background-color: #14428b;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.search-btn:hover {
  filter: brightness(0.9);
  transform: translateY(-2px);
}

.divider {
  height: 1px;
  background-color: var(--border-color);
  width: 100%;
}

.banks-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.banks-label {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-secondary);
}

.banks-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.bank-chip {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.bank-chip:hover {
  background-color: var(--bg-hover);
}

.bank-chip.active {
  background-color: var(--bg-badge);
  color: #4a86e8;
  border-color: #4a86e8;
  font-weight: 700;
}

/* =====================
  4. 컨텐츠 (지도 + 리스트)
===================== */
.content-grid {
  display: flex;
  gap: 24px;
  height: 640px;
}

.map-wrapper {
  flex: 2;
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
}

.map { width: 100%; height: 100%; }

.loc-btn {
  position: absolute;
  top: 20px; right: 20px; z-index: 20;
  width: 44px; height: 44px;
  background: var(--bg-card); 
  border: 1px solid var(--border-color); 
  border-radius: 12px;
  cursor: pointer; font-size: 20px;
  box-shadow: 0 4px 12px var(--shadow-color);
  display: flex; align-items: center; justify-content: center;
  color: var(--text-primary);
}
.loc-btn:hover { background-color: var(--bg-hover); }

.list-wrapper {
  flex: 1;
  background: var(--bg-card);
  border-radius: 24px;
  padding: 24px;
  overflow-y: auto;
  box-shadow: 0 2px 12px var(--shadow-color);
  border: 1px solid var(--border-color);
  display: flex; flex-direction: column;
}

.list-header h3 {
  font-size: 18px; font-weight: 800; color: var(--text-primary); margin-bottom: 20px;
}

.count { color: #4a86e8; }
.loading-text { font-size: 14px; color: var(--text-muted); font-weight: normal; }

.place-list {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 12px;
}

.place-item {
  padding: 16px; border-radius: 16px;
  background-color: var(--bg-card); 
  border: 1px solid var(--border-color);
  cursor: pointer; display: flex; justify-content: space-between; align-items: center;
  transition: all 0.2s;
}

.place-item:hover {
  background-color: var(--bg-hover);
  border-color: #4a86e8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow-color);
}

.place-info { flex: 1; }

.place-title {
  font-size: 16px; font-weight: 700; color: var(--text-primary);
  display: flex; align-items: center; gap: 8px; margin-bottom: 4px;
}

.idx {
  width: 20px; height: 20px; background: #4a86e8; color: white;
  border-radius: 50%; font-size: 11px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

.place-addr { font-size: 13px; color: var(--text-secondary); margin-left: 28px; }
.place-phone { font-size: 13px; color: #4a86e8; margin-left: 28px; margin-top: 2px; }

.route-btn {
  padding: 6px 12px; border-radius: 8px; background-color: var(--bg-badge);
  color: #4a86e8; border: none; font-size: 12px; font-weight: 700; cursor: pointer;
  white-space: nowrap;
}
.route-btn:hover { filter: brightness(0.95); }

/* 검색 결과 없음(Empty State) 영역 스타일 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  color: var(--text-muted, #9ca3af); /* 기존에 정의한 변수가 없다면 기본 회색 사용 */
  background-color: var(--bg-card, #fff); /* 카드 배경색과 맞춤 */
  border-radius: 16px;
  /* 필요하다면 테두리나 그림자 추가 */
  /* border: 1px solid var(--border-color, #e5e7eb); */
}

.empty-icon {
  margin-bottom: 20px;
  color: #d1d5db; /* 아주 연한 회색으로 은은하게 표현 */
  
  /* (선택사항) 마우스 올렸을 때 살짝 움직이는 효과 */
  transition: transform 0.3s ease;
}

.empty-state:hover .empty-icon {
  transform: scale(1.05) rotate(-5deg);
  color: #9ca3af; /* 호버 시 조금 더 진하게 */
}

.empty-state p {
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

/* 스크롤바 커스텀 */
.list-wrapper::-webkit-scrollbar { width: 6px; }
.list-wrapper::-webkit-scrollbar-thumb { background-color: var(--border-color); border-radius: 3px; }

/* =====================
  5. 지도 커스텀 오버레이 (다크모드 강제 적용 필요)
===================== */
.custom-overlay-style {
  position: relative;
  bottom: 45px;
  background-color: var(--bg-card);
  color: var(--text-primary);
  border-radius: 8px;
  padding: 10px 15px;
  box-shadow: 0 2px 10px var(--shadow-color);
  border: 1px solid var(--border-color);
  display: inline-block; 
  white-space: nowrap;
  text-align: center;
}

.custom-overlay-style .title {
  display: block;
  font-weight: bold;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 5px;
}

.custom-overlay-style .info {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
}

/* 말풍선 꼬리 */
.custom-overlay-style::after {
  content: "";
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 10px 8px 0;
  border-style: solid;
  border-color: var(--bg-card) transparent transparent transparent;
  z-index: 1;
}

.custom-overlay-style::before {
  content: "";
  position: absolute;
  bottom: -11px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 10px 8px 0;
  border-style: solid;
  border-color: var(--border-color) transparent transparent transparent;
  z-index: 0;
}
</style>