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

# from django.conf.urls.static import static
# from djangotask import settings

urlpatterns = [
    url(r'^$', views.home_view, name='home'),
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$',
        views.PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/update/$',
        views.update_topic, name='update_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/delete/$',
        views.delete_topic, name='delete_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/delete/(?P<confirmed>\d+)/', views.delete_topic,
        name='delete_topic_confirmed'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$',
        views.reply_topic, name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/export/csv/$',
        views.export_posts_csv, name='export_topics_csv'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/export/xlwt/$',
        views.export_posts_xlwt, name='export_topics_xlwt'),
]
