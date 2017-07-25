# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)
