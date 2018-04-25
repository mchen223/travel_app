# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_auto_20170730_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='user_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_creator', to='log_reg.User'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='user_joiner',
            field=models.ManyToManyField(related_name='user_joiner', to='log_reg.User'),
        ),
    ]
