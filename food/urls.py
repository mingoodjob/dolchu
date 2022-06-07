from django.urls import path
from . import views


urlpatterns = [
    path('main/',views.main_view,name='main_view'),
    path('detail/<int:id>/', views.detail_view, name='detail_view'),
    path('category/<int:id>/', views.category_get, name='category_get'),
    path('search/',views.search, name='search')
]
