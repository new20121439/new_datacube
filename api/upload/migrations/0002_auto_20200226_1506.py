# Generated by Django 3.0 on 2020-02-26 08:06

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='file',
            field=models.FileField(unique=True, upload_to='upload/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['tif'])]),
        ),
        migrations.AlterField(
            model_name='uploadmodel',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('4fb2e164-5773-4fe8-a889-14fc5afc7f35'), unique=True),
        ),
    ]
