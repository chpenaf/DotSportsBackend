# Generated by Django 4.0 on 2022-04-28 17:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0078_alter_member_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 28, 13, 21, 30, 599301)),
        ),
    ]
