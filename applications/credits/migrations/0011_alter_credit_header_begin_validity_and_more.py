# Generated by Django 4.0 on 2022-04-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0010_alter_credit_pos_end_validity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit_header',
            name='begin_validity',
            field=models.DateField(verbose_name='Inicio validez'),
        ),
        migrations.AlterField(
            model_name='credit_header',
            name='end_validity',
            field=models.DateField(verbose_name='Fin validez'),
        ),
        migrations.AlterField(
            model_name='credit_pos',
            name='begin_validity',
            field=models.DateField(verbose_name='Inicio validez'),
        ),
        migrations.AlterField(
            model_name='credit_pos',
            name='end_validity',
            field=models.DateField(verbose_name='Fin validez'),
        ),
    ]