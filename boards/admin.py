from django.contrib import admin
from boards.models import (
    Board, Topic, Post, Log
)

# Register your models here.

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Log)