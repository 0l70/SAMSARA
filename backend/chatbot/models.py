# chatbot/models.py
from django.db import models
from django.conf import settings

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    role = models.CharField(max_length=10)  # 'user' 또는 'ai'
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 날짜/시간 자동 저장

    def __str__(self):
        return f"[{self.created_at}] {self.user.username}: {self.content[:20]}"