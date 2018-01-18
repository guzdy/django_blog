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
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

        # widgets 决定了各个字段在前端渲染的输入框类型
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "名字",
            }),
            'email': forms.TextInput(attrs={
                'placeholder': "邮箱",
            }),
            'body': forms.Textarea(attrs={
                'placeholder': "评论内容",
                'size': '2000'
            })
        }
