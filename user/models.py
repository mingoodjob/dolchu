from django.db import models

# Create your models here.
from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.conf import settings 

class UserModel(AbstractUser): 
    class Meta: db_table = "USER"
