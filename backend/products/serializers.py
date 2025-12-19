from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions

# 예금
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

class DepositProductsSerializer(serializers.ModelSerializer):
    options = DepositOptionsSerializer(many=True, read_only=True) # 옵션 포함해서 출력
    class Meta:
        model = DepositProducts
        fields = '__all__'

# 적금
class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)

class SavingProductsSerializer(serializers.ModelSerializer):
    options = SavingOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = SavingProducts
        fields = '__all__'