# Generated by Django 4.0 on 2022-04-02 01:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0020_alter_location_created_at_alter_pool_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 22, 48, 25, 522178)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 22, 48, 25, 523176)),
        ),
    ]
