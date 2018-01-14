#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-13 下午9:29
# @Author  : guzdy
# @File    : forms.py
from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    # 根据模型（model）创建表单，
    # 我们只需要在这个表单的Meta类里表明使用哪个模型（model）来构建表单。
    # Django将会解析model并为我们动态的创建表单。
    # 每一种模型（model）字段类型都有对应的默认表单字段类型。
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
