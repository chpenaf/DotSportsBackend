# Generated by Django 4.0 on 2022-04-02 00:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_historicaluser_doc_num_alter_user_doc_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='doc_num',
        ),
        migrations.RemoveField(
            model_name='user',
            name='doc_num',
        ),
    ]
