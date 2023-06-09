# Generated by Django 2.2.26 on 2023-03-28 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20230327_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventsVolunteersHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('attended', models.BooleanField()),
                ('daily_total_hours', models.FloatField()),
                ('events_volunteers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.EventsVolunteers')),
            ],
        ),
    ]
