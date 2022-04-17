# Generated by Django 4.0 on 2022-04-16 01:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0052_alter_location_created_at_alter_pool_created_at'),
        ('planning', '0002_calendar_month_label_alter_calendar_day_label_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calendar',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='calendar',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 4, 15, 21, 34, 10, 560996), verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='month_label',
            field=models.CharField(choices=[(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'), (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')], default=(4, 'Abril'), max_length=10, verbose_name='Nombre mes'),
        ),
        migrations.AlterUniqueTogether(
            name='calendar',
            unique_together={('location', 'date')},
        ),
    ]
