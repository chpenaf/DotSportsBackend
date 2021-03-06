# Generated by Django 4.0 on 2022-04-19 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_catalog_courses_alter_catalog_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service_Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(verbose_name='nivel')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.service', verbose_name='Servicio')),
            ],
            options={
                'verbose_name': 'Subcategoría Servicio',
                'verbose_name_plural': 'Subcategorías Servicio',
            },
        ),
    ]
