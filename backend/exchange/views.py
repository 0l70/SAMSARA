from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Exchange
import requests
from datetime import datetime, timedelta  

def update_exchange_rates():
    auth_key = settings.EXCHANGE_API_KEY
    today = datetime.now().date()

    # 오늘부터 6일 전까지 (총 7일) 반복
    for i in range(7):
        # 1. 날짜 계산 (오늘, 어제, 엊그제...)
        target_date = today - timedelta(days=i)
        formatted_date = target_date.strftime("%Y%m%d") # API 요청용 문자열 (예: 20250101)

        # 2. 이미 DB에 해당 날짜 데이터가 있으면 API 호출 건너뛰기 (속도 최적화)
        if Exchange.objects.filter(search_date=target_date).exists():
            continue

        # 3. API 호출
        url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={auth_key}&searchdate={formatted_date}&data=AP01"
        
        try:
            response = requests.get(url, verify=False)
            data = response.json()

            # 주말/공휴일이라 데이터가 없으면 패스
            if not data:
                continue

            # 4. 데이터 저장 (날짜 정보 포함!)
            for item in data:
                clean_rate = item['deal_bas_r'].replace(",", "")
                
                # update_or_create: (통화코드 + 날짜)가 같으면 덮어쓰고, 없으면 새로 만듦
                Exchange.objects.update_or_create(
                    cur_unit=item['cur_unit'],
                    search_date=target_date,   # ★ 날짜를 기준으로 식별합니다
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
        except Exception as e:
            print(f"{formatted_date} 데이터 가져오기 실패: {e}")
            continue

    return True


@api_view(['GET'])
def get_exchange_rates(request):
    # 1. 데이터 업데이트 (없는 날짜만 가져옴)
    update_exchange_rates()

    # 2. DB에서 전체 데이터 가져오기 (날짜 최신순 정렬)
    # 그래프를 그리려면 과거 데이터도 다 필요합니다.
    datas = Exchange.objects.all().order_by('-search_date')
    
    result = []
    for d in datas:
        try:
            rate_float = float(d.deal_bas_r)
        except:
            rate_float = 0.0

        result.append({
            'search_date': d.search_date, # 날짜도 같이 보내줘야 프론트에서 그래프 그림
            'unit': d.cur_unit,
            'name': d.cur_nm,
            'rate': rate_float
        })

    return JsonResponse(result, safe=False)