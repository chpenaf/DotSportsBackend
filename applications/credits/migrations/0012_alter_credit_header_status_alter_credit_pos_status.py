# Generated by Django 4.0 on 2022-05-20 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0011_alter_credit_header_begin_validity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit_header',
            name='status',
            field=models.CharField(choices=[('AC', 'Activo'), ('FI', 'Finalizado'), ('CA', 'Cancelado'), ('EX', 'Expirado')], default='AC', max_length=2, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='credit_pos',
            name='status',
            field=models.CharField(choices=[('AV', 'Disponible'), ('RE', 'Reservado'), ('CO', 'Completado'), ('EX', 'Expirado')], default='AV', max_length=2, verbose_name='Status'),
        ),
    ]
