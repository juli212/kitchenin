# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-05 19:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list', '0004_auto_20170505_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='members',
            field=models.ManyToManyField(related_name='lists', to=settings.AUTH_USER_MODEL),
        ),
    ]
