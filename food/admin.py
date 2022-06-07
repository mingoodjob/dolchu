from django.contrib import admin
from .models import Category, Food, Comment

# Register your models here.
admin.site.register(Food)
admin.site.register(Comment)
admin.site.register(Category)
