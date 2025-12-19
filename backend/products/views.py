from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer
import requests
import os
from dotenv import load_dotenv

load_dotenv() 

api_key = os.getenv('FINANCE_API_KEY')
print(f"API KEY Status: {api_key}")
@api_view(['GET'])
def save_deposit_products(request):
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    
    base_list = response['result']['baseList']
    option_list = response['result']['optionList']

    # 상품 저장
    for base in base_list:
        if not DepositProducts.objects.filter(fin_prdt_cd=base['fin_prdt_cd']).exists():
            serializer = DepositProductsSerializer(data=base)
            if serializer.is_valid():
                serializer.save()

    # 옵션 저장
    for option in option_list:
        product = DepositProducts.objects.filter(fin_prdt_cd=option['fin_prdt_cd']).first()
        if product:
            serializer = DepositOptionsSerializer(data=option)
            if serializer.is_valid():
                serializer.save(product=product)

    return Response({"message": "데이터 저장 성공"})

@api_view(['GET'])
def deposit_products(request):
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many=True)
    return Response(serializer.data)

# ▼▼▼ 적금 데이터 저장 (API_KEY는 위쪽에 이미 선언되어 있어야 함)
@api_view(['GET'])
def save_saving_products(request):
    # 적금 API 주소 (deposit -> saving으로 변경됨)
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    
    base_list = response['result']['baseList']
    option_list = response['result']['optionList']

    for base in base_list:
        if SavingProducts.objects.filter(fin_prdt_cd=base['fin_prdt_cd']).exists():
            continue
        serializer = SavingProductsSerializer(data=base)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for option in option_list:
        product = SavingProducts.objects.filter(fin_prdt_cd=option['fin_prdt_cd']).first()
        if product:
            serializer = SavingOptionsSerializer(data=option)
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=product)

    return Response({"message": "정기적금 데이터 저장 완료!"})

# ▼▼▼ 적금 데이터 조회
@api_view(['GET'])
def saving_products(request):
    products = SavingProducts.objects.all()
    serializer = SavingProductsSerializer(products, many=True)
    return Response(serializer.data)