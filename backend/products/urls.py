from django.urls import path
from . import views

urlpatterns = [
    # 예금
    path('save-deposit-products/', views.save_deposit_products),
    path('deposit-products/', views.deposit_products),
    
    # 적금
    path('save-saving-products/', views.save_saving_products),
    path('saving-products/', views.saving_products),
]