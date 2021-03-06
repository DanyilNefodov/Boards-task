from django.db import models
from accounts.models import UserProfile as User
from django.utils.html import mark_safe
from markdown import markdown
import math


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(
        User, related_name='creator', on_delete=models.DO_NOTHING)
    board = models.ForeignKey(
        Board, related_name='topics', on_delete=models.DO_NOTHING)
    views = models.PositiveIntegerField(default=0)  # <- here

    def __str__(self):
        return "{0} {1}".format(self.subject, str(self.last_updated).split(".")[0])

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 5
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 5

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
    message = models.TextField(max_length=255)
    topic = models.ForeignKey(
        Topic, related_name='posts', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(
        User, null=True, related_name='+', on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0} {1}".format(self.topic, str(self.created_at).split(".")[0][:-20])

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

    def get_photos_of_post(self):
        return Photo.objects.filter(post=self)


class Photo(models.Model):
    post = models.ForeignKey(
        Post, related_name='photos', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to='photos/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


log_kinds = ((0, ("created")),
             (1, ("updated")),
             (2, ("deleted")))


class Log(models.Model):
    topic = models.CharField(max_length=255)
    kind = models.PositiveIntegerField(choices=log_kinds)
    user = models.ForeignKey(User, related_name='logs',
                             on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{0} has been {1} by {2}'.format(self.topic, log_kinds[self.kind][1], self.user)

    def get_kind(self):
        return log_kinds[self.kind][1]
