# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-22 13:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('venues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('date', models.DateField(default=datetime.date.today)),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='venues.Venue')),
            ],
        ),
    ]
