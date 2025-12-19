from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        
        # cleaned_data에서 가져와서 저장
        data = form.cleaned_data
        user.nickname = data.get('nickname')
        user.age = data.get('age')
        user.salary = data.get('salary')
        user.wealth = data.get('wealth')
        user.is_mydata_agreed = data.get('is_mydata_agreed')
        
        user.save()
        return user