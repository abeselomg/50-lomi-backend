# Generated by Django 2.2.26 on 2023-03-24 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20230323_1021'),
        ('events', '0008_auto_20230324_1402'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='eventorganizers',
            unique_together={('event', 'organizer')},
        ),
    ]
