from django.conf.urls import url
from . import views


app_name = 'blogs'

urlpatterns = [
    url(r'^$', views.blog_list, name='list'),
    url(r'^create/$', views.blog_create),
   url(r'^(?P<id>[0-9]+)/$', views.blog_detail, name='detail'),
]