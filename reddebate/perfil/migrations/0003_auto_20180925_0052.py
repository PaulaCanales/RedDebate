# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-25 00:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_auto_20180924_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id_profile',
        ),
        migrations.AddField(
            model_name='userslist',
            name='owner_type',
            field=models.CharField(default='username', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
