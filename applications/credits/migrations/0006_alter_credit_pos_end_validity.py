# Generated by Django 4.0 on 2022-04-19 18:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0005_alter_credit_header_begin_validity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit_pos',
            name='end_validity',
            field=models.DateField(default=datetime.datetime(2022, 5, 19, 14, 46, 4, 644909), verbose_name='Fin validez'),
        ),
    ]