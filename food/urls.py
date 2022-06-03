from django.urls import path
from . import views


urlpatterns = [
    path('main/',views.main_view,name='main_view'),
    path('detail/', views.detail_view, name='detail'),
]


