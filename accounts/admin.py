from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import (
    Hobby, Interest, UserProfile as User, Reader, Blogger,
)

# Register your models here.


class BloggerInline(admin.StackedInline):
    model = Blogger
    can_delete = False
    verbose_name_plural = 'Blogger'
    fk_name = 'user'


class ReaderInline(admin.StackedInline):
    model = Reader
    can_delete = False
    verbose_name_plural = 'Reader'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (BloggerInline, ReaderInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


# admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# admin.site.register(User)
admin.site.register(Hobby)
admin.site.register(Interest)
admin.site.register(Reader)
admin.site.register(Blogger)
