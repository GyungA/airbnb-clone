# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-23 23:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0003_add_verbose_name_and_related_names'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alternativename',
            old_name='language',
            new_name='language_code',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='languages',
            new_name='language_codes',
        ),
    ]
