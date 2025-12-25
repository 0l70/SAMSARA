# backend/accounts/views.py

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User
from rest_framework.authtoken.models import Token 

# ★ 카카오 REST API 키 (settings.py나 .env에 두는 게 좋지만 편의상 여기에 변수로 둡니다)
# 카카오 개발자 센터 > 요약 정보 > REST API 키를 복사해서 아래에 넣으세요!
KAKAO_REST_API_KEY = settings.VITE_KAKAO_REST_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_login(request):
    # 1. 프론트엔드에서 보낸 'code' 받기
    code = request.data.get('code')
    
    if not code:
        return Response({'error': '코드가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # 2. 받은 코드로 카카오에게 '액세스 토큰' 요청하기
    token_url = "https://kauth.kakao.com/oauth/token"
    # redirect_uri = "http://localhost:5173/oauth/callback/kakao" # 등록한 주소와 똑같아야 함!
    redirect_uri = "http://61.73.128.241:5173/oauth/callback/kakao"

    token_data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": redirect_uri,
        "code": code,
    }
    
    token_headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    
    token_res = requests.post(token_url, data=token_data, headers=token_headers)
    token_json = token_res.json()
    
    if "error" in token_json:
        return Response({'error': '카카오 토큰 발급 실패', 'details': token_json}, status=status.HTTP_400_BAD_REQUEST)
        
    access_token = token_json.get('access_token')

    # 3. 액세스 토큰으로 카카오 유저 정보 가져오기
    user_info_url = "https://kapi.kakao.com/v2/user/me"
    user_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    
    user_res = requests.get(user_info_url, headers=user_headers)
    user_info = user_res.json()
    
  
    print("카카오 응답:", user_info) 

    # 4. 정보 파싱 (ID, 닉네임 등)

    kakao_id = user_info.get('id')
    
    # ▼▼▼ 수정된 부분 ▼▼▼
    # kakao_account가 없으면 빈 딕셔너리 {} 를 줘서 에러 방지
    kakao_account = user_info.get('kakao_account', {}) 
    
    # profile이 없으면 빈 딕셔너리 {} 를 주고, 거기서 nickname 찾기
    # 그래도 없으면 'unknown'이라고 이름 붙이기
    profile = kakao_account.get('profile', {})
    nickname = profile.get('nickname', f'user_{kakao_id}')

   

    
    # 5. DB 처리 (심플하게!)
    username = f"kakao_{kakao_id}"

    # ★ 여기서 age, job 등을 안 넣어줘도 모델 설정 덕분에 에러가 안 납니다!
    user, created = User.objects.get_or_create(username=username, defaults={
        'nickname': nickname,
        # age는 자동으로 0, job은 자동으로 Null로 들어갑니다.
    })
    
    if created:
        user.set_unusable_password()
        user.save()

    # 6. 토큰 발급 및 리턴 (mbti와 age도 같이 보내주세요 -> 프론트 판단용)
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'key': token.key,
        'username': user.username,
        'nickname': user.nickname,
        'mbti': user.mbti,
        'age': user.age  # 프론트에서 이 값이 0이면 "정보 입력해주세요"라고 띄우기 위함
    })