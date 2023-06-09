# Generated by Django 2.2.26 on 2023-03-24 09:25

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20230324_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='contact_email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='event',
            name='contact_phone',
            field=models.CharField(default='', max_length=255, validators=[users.utils.validate_phone]),
        ),
    ]
