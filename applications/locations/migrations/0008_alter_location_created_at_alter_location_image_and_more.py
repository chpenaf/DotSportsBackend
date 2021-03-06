# Generated by Django 4.0 on 2022-03-27 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_location_id_city_location_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 27, 17, 25, 23, 302687)),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='locations', verbose_name='Imágen'),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 27, 17, 25, 23, 303687)),
        ),
    ]
