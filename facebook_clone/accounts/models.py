from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    conform_password = models.CharField(max_length=225)


