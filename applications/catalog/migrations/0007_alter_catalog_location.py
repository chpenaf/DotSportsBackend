# Generated by Django 4.0 on 2022-04-22 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0070_alter_location_created_at_alter_pool_created_at'),
        ('catalog', '0006_alter_course_level_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='locations.location', verbose_name='Sede'),
        ),
    ]
