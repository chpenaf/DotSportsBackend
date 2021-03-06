# Generated by Django 4.0 on 2022-04-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre Tecnico')),
                ('path', models.CharField(max_length=50, verbose_name='Ruta')),
                ('icon', models.CharField(max_length=15, verbose_name='Icono')),
                ('text', models.CharField(max_length=30, verbose_name='Titulo')),
                ('admin', models.BooleanField(verbose_name='Administrador')),
                ('staff', models.BooleanField(verbose_name='Empleado')),
                ('member', models.BooleanField(verbose_name='Miembro')),
            ],
            options={
                'verbose_name': 'Aplicación',
                'verbose_name_plural': 'Aplicaciones',
            },
        ),
    ]
