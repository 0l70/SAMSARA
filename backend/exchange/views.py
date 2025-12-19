from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Exchange
import requests
from datetime import datetime  # 👈 1. 이거 꼭 추가하세요!

def update_exchange_rates():
    auth_key = "Md25ygA5zyqsMTkWFvwX3gQDyGUIWEls"
    
    # 👇 2. 날짜를 "오늘"로 자동 설정하는 코드로 변경
    # (YYYYMMDD 형식으로 오늘 날짜를 문자열로 만듭니다)
    search_date = datetime.now().strftime("%Y%m%d")

    # (참고: 주말이나 공휴일에는 데이터가 없어서 API가 빈 값을 줍니다.)
    
    url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={auth_key}&searchdate={search_date}&data=AP01"

    try:
        response = requests.get(url, verify=False)
        data = response.json()

        # 데이터가 비어있으면(주말/공휴일/영업시간 전) 업데이트 안 함
        if not data:
            return False 

        for item in data:
            clean_rate = item['deal_bas_r'].replace(",", "")
            Exchange.objects.update_or_create(
                cur_unit=item['cur_unit'],
                defaults={
                    'cur_nm': item['cur_nm'],
                    'ttb': item['ttb'],
                    'tts': item['tts'],
                    'deal_bas_r': clean_rate,
                    'bkpr': item['bkpr'],
                    'yy_efee_r': item['yy_efee_r'],
                    'ten_dd_efee_r': item['ten_dd_efee_r'],
                    'kftc_bkpr': item['kftc_bkpr'],
                    'kftc_deal_bas_r': item['kftc_deal_bas_r'],
                }
            )
        return True
    
    except Exception as e:
        print(f"에러 발생: {e}")
        return False

# ------------------------------------------------------------
# 2. Vue에서 호출할 API (DB -> Vue 전송)
# ------------------------------------------------------------
@api_view(['GET'])
def get_exchange_rates(request):
    # 1. DB 업데이트 시도 (실무에선 이렇게 매번 하면 느려지니 나중엔 분리하세요)
    update_exchange_rates()

    # 2. DB에서 데이터 가져오기
    # 환율 계산기에는 '통화코드', '국가명', '매매기준율'만 있으면 됩니다.
    datas = Exchange.objects.all()
    
    result = []
    for d in datas:
        # DB에는 CharField로 저장되어 있으므로, 보낼 때는 숫자로(float) 바꿔줍니다.
        try:
            rate_float = float(d.deal_bas_r)
        except:
            rate_float = 0.0 # 변환 실패 시 0

        result.append({
            'unit': d.cur_unit,      # Vue에서 쓸 이름: unit
            'name': d.cur_nm,        # Vue에서 쓸 이름: name
            'rate': rate_float       # Vue에서 쓸 이름: rate (숫자)
        })

    return JsonResponse(result, safe=False)