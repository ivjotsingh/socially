# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models

class User_model(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password=models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on= models.DateTimeField(auto_now=True)

class SessionToken_model(models.Model):
    user=models.ForeignKey(User_model)
    sessionToken=models.CharField(max_length=100)
    is_valid=models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    lastAccessed_on = models.DateTimeField(auto_now=True)

    def createToken(self):
        self.sessionToken=uuid.uuid4()

class Post_model(models.Model):
    user=models.ForeignKey(User_model)
    image=models.FileField(upload_to="user_images")
    image_url=models.CharField(max_length=200)
    caption=models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
