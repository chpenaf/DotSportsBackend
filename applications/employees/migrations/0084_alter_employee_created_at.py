# Generated by Django 4.0 on 2022-05-26 02:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0083_alter_employee_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 25, 22, 36, 57, 891777)),
        ),
    ]
