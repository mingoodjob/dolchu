from django.urls import path
from . import views


urlpatterns = [
    path('main/',views.main_view,name='main_view'),
    path('detail/<int:id>/', views.detail_view, name='detail_view'),
    path('search/',views.search, name='search')
]
