from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(User, related_name='creator', on_delete=models.DO_NOTHING)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.DO_NOTHING)
    views = models.PositiveIntegerField(default=0)  # <- here

    def __str__(self):
        return "{0} {1}".format(self.subject, str(self.last_updated).split(".")[0])


class Post(models.Model):
    message = models.TextField(max_length=255)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0} {1}".format(self.topic, str(self.created_at).split(".")[0][:-20])