# Generated by Django 4.0 on 2022-04-18 15:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0060_alter_location_created_at_alter_pool_created_at'),
        ('employees', '0061_alter_employee_created_at'),
        ('members', '0060_alter_member_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit_Header',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Cantidad')),
                ('begin_validity', models.DateField(default=datetime.date(2022, 4, 18), verbose_name='Inicio validez')),
                ('end_validity', models.DateField(default=datetime.datetime(2022, 5, 18, 11, 0, 2, 535833), verbose_name='Fin validez')),
                ('doc_ref', models.CharField(max_length=30, verbose_name='Documento de referencia')),
                ('entered_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employees.employee')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.location')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='members.member')),
            ],
            options={
                'verbose_name': 'Crédito (cabecera)',
                'verbose_name_plural': 'Créditos (cabecera)',
            },
        ),
        migrations.CreateModel(
            name='Credit_Pos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField(verbose_name='Posición')),
                ('begin_validity', models.DateField(default=datetime.date(2022, 4, 18), verbose_name='Inicio validez')),
                ('end_validity', models.DateField(default=datetime.datetime(2022, 5, 18, 11, 0, 2, 536664), verbose_name='Fin validez')),
                ('status', models.CharField(choices=[('AV', 'Disponible'), ('RE', 'Reservado'), ('CO', 'Completado')], default='AV', max_length=2, verbose_name='Status')),
                ('used_at', models.DateField(blank=True, null=True, verbose_name='Usado el')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.credit_header', verbose_name='Cabecera')),
            ],
            options={
                'verbose_name': 'Crédito (posición)',
                'verbose_name_plural': 'Créditos (posición)',
            },
        ),
    ]
