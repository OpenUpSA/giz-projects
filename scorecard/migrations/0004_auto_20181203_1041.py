# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-12-03 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0003_auto_20181203_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='geo_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scorecard.Geography'),
        ),
    ]