# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-19 22:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0076_metricmodel_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metricmodel',
            name='code',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='metricmodel',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
