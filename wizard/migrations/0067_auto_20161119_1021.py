# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-19 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0066_auto_20161119_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocolmodel',
            name='final_phase_description',
            field=models.TextField(default='Final phase: no new submission, results on test set will be revealed when the organizers make them available.', max_length=2048, verbose_name='Description'),
        ),
    ]
