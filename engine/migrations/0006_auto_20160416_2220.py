# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-17 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0005_auto_20160405_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.CharField(max_length=150),
        ),
    ]
