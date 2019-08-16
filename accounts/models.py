from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Avatar(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='avatars/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'avatar'
        verbose_name_plural = 'avatars'


class UserProfile(AbstractUser):
    # name = models.CharField(max_length=100)
    # surmane = models.CharField(max_length=100)
    is_blogger = models.BooleanField(default=False)
    is_reader = models.BooleanField(default=False)
    avatar = models.ForeignKey(
        Avatar, related_name='avatar', on_delete=models.CASCADE, null=True)


class Hobby(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Blogger(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='blogger')
    birth_day = models.DateField()
    country = models.CharField(max_length=100)
    hobbies = models.ManyToManyField(Hobby)


class Interest(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Reader(models.Model):
    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='reader')
    interests = models.ManyToManyField(Interest)
    status = models.CharField(max_length=255)


@receiver(post_save, sender=UserProfile)
def create_or_update_reader_profile(sender, instance, created, **kwargs):
    pass
    # if created and sender.is_reader:
    #     Reader.objects.create(user=instance)
    # instance.save()


@receiver(post_save, sender=UserProfile)
def create_or_update_blogger_profile(sender, instance, created, **kwargs):
    pass
    # if created and sender.is_blogger:
    #     Blogger.objects.create(user=instance)
    # instance.save()
