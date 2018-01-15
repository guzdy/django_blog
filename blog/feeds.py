#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-1-15 下午5:12
# @Author  : guzdy
# @File    : feeds.py
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostsFeed(Feed):
    title = 'My Blog'
    link = '/blog/'
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

