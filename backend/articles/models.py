from django.db import models
from django.conf import settings  # 유저 모델 연결을 위해 필수

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ▼▼▼ [핵심] 이 클래스가 없어서 에러가 난 것입니다. 추가해주세요! ▼▼▼
class Comment(models.Model):
    # 1. 누가 썼는지 (User 연결)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 2. 어떤 글에 썼는지 (Article 연결)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    # 3. 내용
    content = models.TextField()
    # 4. 시간
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content