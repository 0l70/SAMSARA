from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list),
    
    # ▼▼▼ 이 한 줄로 조회(GET), 삭제(DELETE), 수정(PUT) 다 처리합니다.
    path('<int:article_pk>/', views.article_detail),
    
    path('<int:article_pk>/comments/', views.comment_create),
    path('comments/<int:comment_pk>/', views.comment_delete),
]