from unicodedata import category
from django.db import models
from user.models import UserModel


class Comment(models.Model):
    class Meta:
        db_table = "comments"

    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # store = models.ForeignKey(FoodModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    star = models.FloatField()

class Food(models.Model):
    class Meta:
        db_table = "food"

    store =  models.CharField(max_length=256)
    img =  models.CharField(max_length=256)
    address =  models.CharField(max_length=256)
    tel =  models.CharField(max_length=256)
    price =  models.CharField(max_length=256)
    parking =  models.CharField(max_length=256)
    close =  models.CharField(max_length=256)
    holliday =  models.CharField(max_length=256)
    staravg =  models.IntegerField(max_length=256)



