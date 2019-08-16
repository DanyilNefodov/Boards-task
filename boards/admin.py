from django.contrib import admin
from boards.models import (
    Board, Topic, Post, Log, Photo
)

# Register your models here.


def activate_boards(modeladmin, request, queryset):
    for board in queryset:
        board.active = True
        board.save()


def deactivate_boards(modeladmin, request, queryset):
    for board in queryset:
        board.active = False
        board.save()


class BoardAdmin(admin.ModelAdmin):
    actions = [activate_boards, deactivate_boards, ]


activate_boards.short_description = 'Activate boards'
deactivate_boards.short_description = 'Deactivate boards'
admin.site.register(Board, BoardAdmin)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Log)
admin.site.register(Photo)
