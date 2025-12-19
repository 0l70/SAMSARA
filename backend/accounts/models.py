from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nickname = models.CharField(max_length=20, null=True)
    # 추가 필드
    age = models.IntegerField(default=0, verbose_name="나이")
    salary = models.IntegerField(default=0, verbose_name="연봉")
    wealth = models.IntegerField(default=0, verbose_name="자산")
    is_mydata_agreed = models.BooleanField(default=False, verbose_name="마이데이터 동의")
    # 찜한 상품 (M:N 관계)
    financial_products = models.TextField(blank=True, null=True)