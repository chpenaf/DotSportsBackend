# Generated by Django 4.0 on 2022-04-22 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_remove_courseschedule_endtime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursesession',
            old_name='course_asigned',
            new_name='course_assigned',
        ),
    ]