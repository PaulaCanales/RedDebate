# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-07-15 18:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumen', '0022_argumento_usa_alias'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='argumento',
            name='usa_alias',
        ),
    ]