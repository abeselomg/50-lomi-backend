# Generated by Django 2.2.26 on 2023-03-27 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20230326_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventsvolunteers',
            old_name='volunteers',
            new_name='volunteer',
        ),
    ]
