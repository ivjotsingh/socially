# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0015_auto_20170803_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='review',
            field=models.FloatField(default=0.7),
        ),
    ]
