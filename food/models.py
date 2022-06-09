from unicodedata import category
from django.db import models
from user.models import UserModel

class Category(models.Model):
    class Meta:
        db_table = "categorys"
    
    category = models.CharField(max_length=256)
    desc = models.TextField(max_length=256, blank=True)

class Food(models.Model):
    class Meta:
        db_table = "foods"

    store = models.CharField(max_length=256)
    img = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    tel = models.CharField(max_length=256, blank=True)
    price = models.CharField(max_length=256, blank=True)
    parking = models.CharField(max_length=256, blank=True)
    close = models.CharField(max_length=256, blank=True)
    holiday = models.CharField(max_length=256, blank=True)
    staravg = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    class Meta:
        db_table = "comments"

    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # store = models.ForeignKey(Food, on_delete=models.CASCADE)
    store = models.ForeignKey(Food, on_delete=models.CASCADE)

    comment = models.CharField(max_length=256)
    star = models.FloatField()

class Travel(models.Model):

    class Meta:
        db_table = "travels"

    travel_title = models.CharField(max_length=256)
    travel_img = models.CharField(max_length=256)
    region = models.CharField(max_length=256)    



