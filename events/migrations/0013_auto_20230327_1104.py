# Generated by Django 2.2.26 on 2023-03-27 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20230327_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsvolunteers',
            name='status',
            field=models.CharField(choices=[('registered', 'registered'), ('unregistered', 'unregistered')], max_length=255),
        ),
    ]
