# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumen', '0012_auto_20161208_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='argumento',
            name='alias_c',
            field=models.CharField(default='username', max_length=50),
        ),
    ]
