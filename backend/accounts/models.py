from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=20, null=True)
    # 추가 필드
    age = models.IntegerField(default=0, verbose_name="나이")
    # ▼ 추가된 필드들
    gender = models.CharField(max_length=10, null=True, blank=True)   # 남성/여성
    job = models.CharField(max_length=20, null=True, blank=True)      # 학생/직장인...
    income_source = models.CharField(max_length=20, null=True, blank=True) # 월급/용돈...
    mbti = models.CharField(max_length=10, null=True, blank=True)
    
    is_mydata_agreed = models.BooleanField(default=False, verbose_name="마이데이터 동의")
    # 찜한 상품 (M:N 관계)
    financial_products = models.TextField(blank=True, null=True)