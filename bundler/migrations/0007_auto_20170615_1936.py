# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-15 19:36
from __future__ import unicode_literals

import chalab.tools.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bundler', '0006_auto_20160922_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundletaskmodel',
            name='output',
            field=models.FileField(null=True, storage=chalab.tools.storage.OverwriteStorage(), upload_to=chalab.tools.storage.save_to_bundle),
        ),
    ]
