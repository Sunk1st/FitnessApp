# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueSquirrelsFitnessApp', '0002_auto_20160930_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
        ),
    ]
