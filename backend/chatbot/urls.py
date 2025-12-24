from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('history/', views.get_chat_history, name='get_chat_history'),
]