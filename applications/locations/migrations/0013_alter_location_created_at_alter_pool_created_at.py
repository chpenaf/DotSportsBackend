# Generated by Django 4.0 on 2022-04-02 00:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0012_alter_location_canceled_by_alter_location_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 21, 27, 11, 142348)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 21, 27, 11, 142348)),
        ),
    ]