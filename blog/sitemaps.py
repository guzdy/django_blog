#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-1-15 下午4:39
# @Author  : guzdy
# @File    : sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # changefreq和priority属性表明了帖子页面修改的频率和它们在网站中的关联性（最大值是1）。
    # items()方法返回了在这个站点地图（sitemap）中所包含对象的查询集（QuerySet）。
    # 默认的，Django在每个对象中调用get_absolute_url()方法来获取它的URL。
    # lastmode方法接收items()返回的每一个对象并且返回对象的最后修改时间。
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish


