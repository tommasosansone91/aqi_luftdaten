# Generated by Django 2.2.8 on 2020-04-23 20:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pm_lookup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target_area_output_data',
            name='Last_update_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
