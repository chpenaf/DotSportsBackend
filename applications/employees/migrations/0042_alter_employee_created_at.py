# Generated by Django 4.0 on 2022-04-13 21:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0041_alter_employee_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 13, 17, 56, 26, 149921)),
        ),
    ]
