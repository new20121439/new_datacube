# Generated by Django 3.0.3 on 2020-02-26 14:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_auto_20200226_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('80e9046d-2091-42d6-a0c7-aa54d5c2628d'), unique=True),
        ),
    ]
