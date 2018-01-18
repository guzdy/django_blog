#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-13 下午3:39
# @Author  : guzdy
# @File    : urls.py
from django.conf.urls import url, include
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    #url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^tag/(?P<tag_slug>[\w-]+)/$', views.TagView.as_view(),
        name='tag'),
    url(r'^category/(?P<category_slug>[\w-]+)/$', views.CategoryView.as_view(),
        name='category'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',
        views.ArchivesView.as_view(), name='archives'),
    url(r'^post/(?P<slug>[-\w]+)/$', views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
]