# Generated by Django 4.0 on 2022-04-16 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0004_calendar_daytype_alter_calendar_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='date',
            field=models.DateField(default=datetime.date(2022, 4, 16), verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day',
            field=models.IntegerField(default=16, verbose_name='Día'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day_label',
            field=models.CharField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (7, 'Domingo')], default=(6, 'Sábado'), max_length=10, verbose_name='Nombre día'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day_week',
            field=models.IntegerField(default=6, verbose_name='Día de la semana'),
        ),
    ]