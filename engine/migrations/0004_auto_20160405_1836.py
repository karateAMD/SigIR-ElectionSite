# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-05 18:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0003_auto_20160405_1819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='searchterm',
            options={'ordering': ('text',)},
        ),
    ]