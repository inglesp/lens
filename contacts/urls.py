from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.search, name='search'),
    url(r'^all$', views.all, name='all'),
)