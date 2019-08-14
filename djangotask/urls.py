"""djangotask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from boards import views as views
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from djangotask import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('boards.urls')),
    url(r'^', include('accounts.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^info/', include('django.contrib.flatpages.urls')),
    url(r'^putin/(?P<boards_>\d+)/(?P<topics_>\d+)/(?P<posts_>\d+)/',
        views.put_in_boards, name='putin'),
    url(r'^send/', views.send_mail_view, name='send')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
