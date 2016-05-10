# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-08 19:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movierec', '0002_auto_20160508_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='occ',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='pin',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.IntegerField(default=100),
        ),
    ]
