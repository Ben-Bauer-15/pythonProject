# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-26 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0004_auto_20181026_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='notes',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='set',
            name='reps',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='set',
            name='result',
            field=models.IntegerField(default=0),
        ),
    ]
