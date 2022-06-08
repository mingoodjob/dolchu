from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dbsave/', views.dbsave, name='dbsave'),
    path('randomreview/', views.random_review, name='random_review'),
    path('category_create/', views.category_create, name='category_create'),
    path('randomuser/', views.user_create, name='user_create'),
]