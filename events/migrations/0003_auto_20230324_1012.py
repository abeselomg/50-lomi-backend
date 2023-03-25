# Generated by Django 2.2.26 on 2023-03-24 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventorganizers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('upcoming', 'upcoming'), ('ongoing', 'ongoing'), ('canceled', 'canceled'), ('postponed', 'postponed'), ('finished', 'finished')], default='upcoming', max_length=255),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]