# Generated by Django 4.0 on 2022-04-16 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0054_alter_member_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 16, 16, 11, 44, 434834)),
        ),
    ]