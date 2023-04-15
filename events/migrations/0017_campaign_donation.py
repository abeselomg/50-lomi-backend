# Generated by Django 2.2.26 on 2023-03-28 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0006_auto_20230323_1021'),
        ('events', '0016_auto_20230328_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('starting_date', models.DateField()),
                ('ending_date', models.DateField()),
                ('campaign_manger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('donation_date', models.DateField(auto_now_add=True)),
                ('campaign', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.Campaign')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Organization')),
            ],
        ),
    ]