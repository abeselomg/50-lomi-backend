# Generated by Django 2.2.26 on 2023-03-28 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_eventsvolunteershours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsvolunteers',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
