# Generated by Django 3.0 on 2020-02-24 03:06

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('uuid', models.UUIDField(default=uuid.UUID('8bb563e3-6bf9-4360-8bf8-62883505ddbf'), unique=True)),
                ('product_name', models.CharField(choices=[('uav', 'UAV')], max_length=100)),
                ('file', models.FileField(upload_to='upload', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['tif'])])),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-upload_time'],
            },
        ),
    ]
