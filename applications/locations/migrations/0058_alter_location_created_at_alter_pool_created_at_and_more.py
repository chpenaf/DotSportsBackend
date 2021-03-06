# Generated by Django 4.0 on 2022-04-18 00:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0057_rename_id_location_pool_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 17, 20, 23, 17, 986216)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 17, 20, 23, 17, 986943)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.location', verbose_name='Sedes'),
        ),
    ]
