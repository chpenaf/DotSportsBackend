# Generated by Django 4.0 on 2022-04-12 19:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0034_alter_location_created_at_alter_pool_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 12, 15, 13, 0, 294438)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 12, 15, 13, 0, 295395)),
        ),
    ]
