# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-05 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0002_auto_20160404_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='last_name',
            field=models.CharField(default='', max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='searchterm',
            name='text',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
