# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 04:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20171013_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
    ]
