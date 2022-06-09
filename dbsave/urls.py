from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dbsave/', views.dbsave, name='dbsave'),
    path('randomreview/', views.random_review, name='random_review'),
    path('category_create/', views.category_create, name='category_create'),
    path('randomuser/', views.user_create, name='user_create'),
    path('staravg/', views.star_avg, name='star_avg'),
    path('travel', views.travel, name='travel'),
    path('travel_create/', views.travel_create, name='travel_create'),
    path('travel_save/', views.travel_save, name='travel_save'),
]
