# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-23 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20170518_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='old_status',
            field=models.IntegerField(blank=True, choices=[(1, 'need'), (2, 'pantry'), (3, 'fridge'), (4, 'gone')]),
        ),
    ]
