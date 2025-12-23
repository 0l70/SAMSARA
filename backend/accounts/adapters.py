from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        
        # ▼ 수정: salary, wealth 삭제 -> 새 필드 추가
        user.nickname = data.get('nickname')
        user.age = data.get('age')
        user.gender = data.get('gender')
        user.job = data.get('job')
        user.income_source = data.get('income_source')
        user.mbti = data.get('mbti')
        user.is_mydata_agreed = data.get('is_mydata_agreed')
        
        user.save()
        return user