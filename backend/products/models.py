from django.db import models

# 예금
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 상품코드
    kor_co_nm = models.TextField() # 은행명
    fin_prdt_nm = models.TextField() # 상품명
    etc_note = models.TextField() # 유의사항
    join_deny = models.IntegerField() # 가입제한
    join_member = models.TextField() # 가입대상
    join_way = models.TextField() # 가입방법
    spcl_cnd = models.TextField() # 우대조건

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100) # 금리유형
    intr_rate = models.FloatField(null=True) # 기본금리
    intr_rate2 = models.FloatField(null=True) # 우대금리
    save_trm = models.IntegerField() # 저축기간

# 적금
class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융상품명
    etc_note = models.TextField()               # 기타 유의사항
    join_deny = models.IntegerField()           # 가입제한
    join_member = models.TextField()            # 가입대상
    join_way = models.TextField()               # 가입방법
    spcl_cnd = models.TextField()               # 우대조건

class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100) # 금리유형
    intr_rate = models.FloatField(null=True)             # 저축 금리
    intr_rate2 = models.FloatField(null=True)            # 최고 우대 금리
    save_trm = models.IntegerField()                     # 저축 기간
    rsrv_type_nm = models.TextField()                    # 적립 유형 (자유적립식/정액적립식)