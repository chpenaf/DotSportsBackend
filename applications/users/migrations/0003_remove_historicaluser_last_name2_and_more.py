# Generated by Django 4.0 on 2021-12-08 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_historicaluser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='last_name2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name2',
        ),
    ]
