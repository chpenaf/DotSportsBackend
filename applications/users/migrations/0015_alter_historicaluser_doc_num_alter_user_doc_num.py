# Generated by Django 4.0 on 2022-04-02 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_historicaluser_doc_num_alter_user_doc_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='doc_num',
            field=models.CharField(db_index=True, max_length=10, null=True, verbose_name='N° Documento'),
        ),
        migrations.AlterField(
            model_name='user',
            name='doc_num',
            field=models.CharField(max_length=10, null=True, unique=True, verbose_name='N° Documento'),
        ),
    ]