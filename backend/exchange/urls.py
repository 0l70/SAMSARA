from django.urls import path
from . import views

urlpatterns = [
    # Vue에서 axios로 요청할 주소
    path('exchange-rates/', views.get_exchange_rates),
    path('gold-silver/', views.get_gold_silver_price),
]