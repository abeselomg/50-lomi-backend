# Generated by Django 2.2.26 on 2023-04-26 12:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20230406_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCertificate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='eventsvolunteerscertification',
            name='description',
        ),
        migrations.RemoveField(
            model_name='eventsvolunteerscertification',
            name='title',
        ),
        migrations.AlterField(
            model_name='eventsvolunteerscertification',
            name='events_volunteers',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.EventsVolunteers'),
        ),
        migrations.AddField(
            model_name='eventsvolunteerscertification',
            name='event_certeficate',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.EventCertificate'),
        ),
    ]
