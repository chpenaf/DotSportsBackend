# Generated by Django 4.0 on 2022-04-02 00:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_historicaluser_avatar_user_avatar'),
        ('locations', '0011_location_canceled_at_location_canceled_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='canceled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_canceled_by', to='users.user'),
        ),
        migrations.AlterField(
            model_name='location',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 21, 25, 20, 846718)),
        ),
        migrations.AlterField(
            model_name='pool',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 1, 21, 25, 20, 848718)),
        ),
    ]
