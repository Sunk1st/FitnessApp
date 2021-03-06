# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueSquirrelsFitnessApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='calories',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='food',
            name='carbohydrates',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='food',
            name='lipids',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='food',
            name='protein',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='food',
            name='sugar',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
