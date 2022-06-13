from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('category_create/', views.category_create, name='category_create'), #1
    path('dbpush/', views.dbpush, name='dbpush'), #2
    path('randomuser/', views.user_create, name='user_create'), #3
    path('randomreview/', views.random_review, name='random_review'), #4
    path('staravg/', views.star_avg, name='star_avg'), #5
    path('travel_save/', views.travel_save, name='travel_save'), #6
    path('review_load/', views.review_load, name='review_load'), #7
]
