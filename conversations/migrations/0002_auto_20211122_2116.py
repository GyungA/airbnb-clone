# Generated by Django 2.2.5 on 2021-11-22 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='messafe',
            new_name='message',
        ),
    ]
