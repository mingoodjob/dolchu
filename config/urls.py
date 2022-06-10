from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('',include('user.urls')),
    path('',include('dbsave.urls')),
    path('',include('recommand.urls')),
]


