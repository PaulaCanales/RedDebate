# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-14 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0011_listado_usuariolistado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuariolistado',
            old_name='creador',
            new_name='usuario',
        ),
    ]