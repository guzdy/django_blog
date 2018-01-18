#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-1-14 下午10:34
# @Author  : guzdy
# @File    : blog_tags.py
from django import template
from ..models import Post, Category, Tag
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


# 每一个模板标签（template tags）都需要包含一个叫做register的变量来表明
# 自己是一个有效的标签（tag）库。这个变量是template.Library的一个实例
register = template.Library()


# simple_tag：处理数据并返回一个字符串（string）kl
@register.simple_tag
def total_posts():
    return Post.published.count()


@register.simple_tag
def show_latest_posts(count=4):
    return Post.published.order_by('-publish')[:count]


@register.simple_tag
def get_most_commented_posts(count=4):
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments')[:count]


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def archives():
    # 这个 dates 方法会返回一个列表，列表中的元素为每一篇 Post 创建的时间，精确到月份，降序排列
    return Post.objects.dates('publish', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.all()
