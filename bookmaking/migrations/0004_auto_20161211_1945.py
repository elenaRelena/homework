# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-11 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmaking', '0003_horse_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horse',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
