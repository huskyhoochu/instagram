# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(blank=True, to='post.Post', verbose_name='좋아요 누른 포스트 목록'),
        ),
    ]
