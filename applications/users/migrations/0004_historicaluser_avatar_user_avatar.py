# Generated by Django 4.0 on 2021-12-09 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_historicaluser_last_name2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaluser',
            name='avatar',
            field=models.TextField(max_length=100, null=True, verbose_name='Avatar'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to='users', verbose_name='Avatar'),
        ),
    ]
