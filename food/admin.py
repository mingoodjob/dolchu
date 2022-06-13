from django.contrib import admin
from .models import Category, Food, Comment,Travel

# Register your models here.
admin.site.register(Food)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Travel)
