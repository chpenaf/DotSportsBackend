# Generated by Django 4.0 on 2022-05-26 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0014_alter_calendar_day_alter_calendar_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='day',
            field=models.IntegerField(default=25, verbose_name='Día'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day_label',
            field=models.CharField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (7, 'Domingo')], default=(3, 'Miércoles'), max_length=10, verbose_name='Nombre día'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day_week',
            field=models.IntegerField(default=3, verbose_name='Día de la semana'),
        ),
    ]
