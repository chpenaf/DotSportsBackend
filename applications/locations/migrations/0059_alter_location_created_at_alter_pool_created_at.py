# Generated by Django 4.0 on 2022-04-18 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0058_alter_location_created_at_alter_pool_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 18, 8, 59, 59, 263819)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 18, 8, 59, 59, 264817)),
        ),
    ]
