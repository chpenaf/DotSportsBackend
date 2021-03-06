# Generated by Django 4.0 on 2022-04-17 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0006_alter_calendar_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='day',
            field=models.IntegerField(default=17, verbose_name='Día'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day_label',
            field=models.CharField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (7, 'Domingo')], default=(7, 'Domingo'), max_length=10, verbose_name='Nombre día'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='day_week',
            field=models.IntegerField(default=7, verbose_name='Día de la semana'),
        ),
    ]
