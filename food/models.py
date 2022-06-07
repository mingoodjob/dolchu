from unicodedata import category
from django.db import models
from user.models import UserModel


class Food(models.Model):
    class Meta:
        db_table = "food"

    store = models.CharField(max_length=256)
    img = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    tel = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    parking = models.CharField(max_length=256)
    close = models.CharField(max_length=256)
    holiday = models.CharField(max_length=256)
    staravg = models.FloatField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    category = models.CharField(max_length=256)

class Comment(models.Model):
    class Meta:
        db_table = "comments"

    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # store = models.ForeignKey(Food, on_delete=models.CASCADE)
    store = models.CharField(max_length=256)

    comment = models.CharField(max_length=256)
    star = models.FloatField()




