# Generated by Django 4.0 on 2022-04-19 17:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0064_alter_employee_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 19, 13, 47, 27, 87409)),
        ),
    ]
