# Generated by Django 2.2.26 on 2023-03-26 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20230324_1528'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventsvolunteers',
            old_name='Registery_date',
            new_name='registery_date',
        ),
    ]
