from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('recommand/', views.recommand, name='recommand'), #추천시스템
]
