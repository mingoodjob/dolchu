from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('dbsave/', views.dbsave, name='dbsave'), #2
    path('randomreview/', views.random_review, name='random_review'), #4
    path('category_create/', views.category_create, name='category_create'), #1
    path('randomuser/', views.user_create, name='user_create'), #3
    path('staravg/', views.star_avg, name='star_avg'), #5
    path('travel', views.travel, name='travel'), 
    path('travel_create/', views.travel_create, name='travel_create'),
    path('travel_save/', views.travel_save, name='travel_save'), #6
    path('review_load/', views.review_load, name='review_load'), #7
    path('recommand/', views.recommand, name='recommand'), #추천시스템
]
