from django.db import models
from django.contrib.auth.models import AbstractUser
from djangotask.settings import AUTH_USER_MODEL as User

# Create your models here.


class UserProfile(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Hobby(models.Model):
    title = models.CharField(max_length=40)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='blogger')
    birth_day = models.DateField()
    country = models.CharField(max_length=100)
    hobbies = models.ManyToManyField(Hobby)


class Interest(models.Model):
    title = models.CharField(max_length=40)


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='reader')
    hobbies = models.ManyToManyField(Interest)
    status = models.CharField(max_length=255)
