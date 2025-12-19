from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Exchange
import requests
from datetime import datetime, timedelta  
import os
import yfinance as yf
import json

BACKUP_FILE_PATH = os.path.join(settings.BASE_DIR, 'gold_silver_backup.json')

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

@api_view(['GET'])
def get_gold_silver_price(request):
    print("✨ 금/은 시세 요청 들어옴!")
    
    try:
        # 1. 야후 파이낸스에서 실시간 데이터 긁어오기 (최근 1달)
        # 타임아웃 5초 설정 (5초 안에 답 없으면 에러로 간주)
        gold = yf.Ticker("GC=F")
        silver = yf.Ticker("SI=F")
        
        gold_hist = gold.history(period="1mo")
        silver_hist = silver.history(period="1mo")

        # 데이터가 비어있으면 에러 발생시키기 (백업본 쓰도록)
        if gold_hist.empty or silver_hist.empty:
            raise Exception("데이터가 비어있습니다.")

        data = []
        for date, row in gold_hist.iterrows():
            date_str = date.strftime('%Y-%m-%d')
            silver_price = 0
            if date in silver_hist.index:
                silver_price = silver_hist.loc[date]['Close']

            data.append({
                'date': date_str,
                'gold': round(row['Close'], 2),
                'silver': round(silver_price, 2)
            })

        # 2. 성공했으므로 JSON 파일에 백업(저장)해두기 💾
        with open(BACKUP_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print("✅ 실시간 데이터 로딩 성공 (백업 완료)")
        return Response(data)

    except Exception as e:
        # 3. 실패했을 경우 (인터넷 끊김, 야후 서버 다운 등) -> 백업 파일 읽기
        print(f"❌ 실시간 로딩 실패! 백업 데이터를 사용합니다. (에러: {e})")
        
        if os.path.exists(BACKUP_FILE_PATH):
            with open(BACKUP_FILE_PATH, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            return Response(backup_data)
        else:
            # 백업 파일조차 없으면 빈 배열 리턴
            return Response([])