#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-13 下午9:29
# @Author  : guzdy
# @File    : forms.py
from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


