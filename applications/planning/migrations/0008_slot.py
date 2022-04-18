# Generated by Django 4.0 on 2022-04-18 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0007_alter_calendar_day_alter_calendar_day_label_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.IntegerField(verbose_name='Slot')),
                ('starttime', models.TimeField(verbose_name='Inicio')),
                ('endtime', models.TimeField(verbose_name='Fin')),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='planning.calendar')),
            ],
            options={
                'verbose_name': 'Slot',
                'verbose_name_plural': 'Slots',
            },
        ),
    ]