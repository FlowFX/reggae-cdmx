# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reggae_cdmx', '0006_auto_20170314_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reggae_cdmx.Venue'),
        ),
    ]