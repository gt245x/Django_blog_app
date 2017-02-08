from django.conf.urls import url
from . import views


app_name = 'blogs'

urlpatterns = [
    url(r'^$', views.blog_list, name='list'),
    url(r'^create/$', views.blog_create, name='create'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^(?P<slug>[\w-]+)/$', views.blog_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit$', views.blog_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete$', views.blog_delete, name='delete'),

]