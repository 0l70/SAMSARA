from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

# 1. 회원가입 시 추가 데이터를 처리할 시리얼라이저
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False)
    age = serializers.IntegerField(required=True)
    salary = serializers.IntegerField(required=True)
    wealth = serializers.IntegerField(required=True)
    is_mydata_agreed = serializers.BooleanField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['age'] = self.validated_data.get('age', 0)
        data['salary'] = self.validated_data.get('salary', 0)
        data['wealth'] = self.validated_data.get('wealth', 0)
        data['is_mydata_agreed'] = self.validated_data.get('is_mydata_agreed', False)
        return data

# 2. 유저 정보를 조회할 때(프로필 등) 보여줄 시리얼라이저
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'age', 'salary', 'wealth', 'is_mydata_agreed')