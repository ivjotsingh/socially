# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from social.models import UserModel,PostModel,TagModel

admin.site.register(UserModel)
admin.site.register(PostModel)
admin.site.register(TagModel)