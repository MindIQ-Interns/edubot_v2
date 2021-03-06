# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizbot', '0002_auto_20160704_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='fb_id',
            field=models.CharField(default='0', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='botuser',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
