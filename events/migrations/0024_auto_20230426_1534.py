# Generated by Django 2.2.26 on 2023-04-26 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_auto_20230426_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsvolunteerscertification',
            name='event_certeficate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.EventCertificate'),
        ),
        migrations.AlterField(
            model_name='eventsvolunteerscertification',
            name='events_volunteers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.EventsVolunteers'),
        ),
    ]
