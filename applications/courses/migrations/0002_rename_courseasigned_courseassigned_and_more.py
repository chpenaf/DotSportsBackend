# Generated by Django 4.0 on 2022-04-22 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0071_alter_location_created_at_alter_pool_created_at'),
        ('catalog', '0007_alter_catalog_location'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseAsigned',
            new_name='CourseAssigned',
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='weekday',
            field=models.IntegerField(choices=[(1, 'Lunes'), (2, 'Martes'), (3, 'Miércoles'), (4, 'Jueves'), (5, 'Viernes'), (6, 'Sábado'), (7, 'Domingo')], default=1, verbose_name='Día de la semana'),
        ),
    ]
