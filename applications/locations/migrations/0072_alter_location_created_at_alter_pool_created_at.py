# Generated by Django 4.0 on 2022-04-22 14:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0071_alter_location_created_at_alter_pool_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 22, 10, 52, 47, 748437)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 22, 10, 52, 47, 748437)),
        ),
    ]
