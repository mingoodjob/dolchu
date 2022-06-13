from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('mypage/<username>/', views.mypage_view, name='mypage'),
]