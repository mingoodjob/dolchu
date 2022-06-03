from django.db import models
from user.models import UserModel


class Comment(models.Model):
    class Meta:
        db_table = "comments"

    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # store = models.ForeignKey(FoodModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)
    star = models.FloatField()