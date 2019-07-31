from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Hobby(models.Model):
    title = models.CharField(max_length=40)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_day = models.DateField()
    country = models.CharField(max_length=100)
    hobbies = models.ManyToManyField(Hobby)


class Interest(models.Model):
    title = models.CharField(max_length=40)


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hobbies = models.ManyToManyField(Interest)
    status = models.CharField(max_length=255)
