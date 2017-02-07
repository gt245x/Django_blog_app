from django.conf.urls import url
from . import views


app_name = 'blogs'

urlpatterns = [
    url(r'^$', views.blog_list, name='list'),
    url(r'^create/$', views.blog_create, name='create'),
    url(r'^(?P<id>[0-9]+)/$', views.blog_detail, name='detail'),
    url(r'^(?P<id>[0-9]+)/edit$', views.blog_update, name='update'),
    url(r'^(?P<id>[0-9]+)/delete$', views.blog_delete, name='delete'),
]