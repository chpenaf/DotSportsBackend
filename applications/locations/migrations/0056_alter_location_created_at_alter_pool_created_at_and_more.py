# Generated by Django 4.0 on 2022-04-16 21:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0055_alter_location_created_at_alter_pool_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 16, 17, 37, 57, 125447)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 16, 17, 37, 57, 126153)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
