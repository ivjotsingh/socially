# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from social.models import UserModel,PostModel,TagModel,FetchModel

admin.site.register(UserModel)
admin.site.register(PostModel)
admin.site.register(TagModel)
admin.site.register((FetchModel))