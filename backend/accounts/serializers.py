from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

# 1. 회원가입 시: 입력받은 데이터를 검증하는 역할
class CustomRegisterSerializer(RegisterSerializer):
    # ▼ 삭제: salary, wealth
    # ▼ 추가: 새로 만든 필드들
    nickname = serializers.CharField(required=False)
    age = serializers.IntegerField(required=True)
    gender = serializers.CharField(required=True)
    job = serializers.CharField(required=True)
    income_source = serializers.CharField(required=True)
    mbti = serializers.CharField(required=False, allow_blank=True, allow_null=True) # 없어도 됨
    is_mydata_agreed = serializers.BooleanField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        # 데이터 포장 (여기서 딕셔너리로 만들어서 어댑터로 넘김)
        data.update({
            'nickname': self.validated_data.get('nickname', ''),
            'age': self.validated_data.get('age', 0),
            'gender': self.validated_data.get('gender', ''),
            'job': self.validated_data.get('job', ''),
            'income_source': self.validated_data.get('income_source', ''),
            'mbti': self.validated_data.get('mbti', ''),
            'is_mydata_agreed': self.validated_data.get('is_mydata_agreed', False),
        })
        return data

# 2. 프로필 조회 시: DB 데이터를 JSON으로 보여주는 역할
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # ▼ salary, wealth 삭제하고 새 필드 추가
        fields = (
            'id', 'username', 'email', 'nickname', 
            'age', 'gender', 'job', 'income_source', 'mbti', 
            'is_mydata_agreed'
        )