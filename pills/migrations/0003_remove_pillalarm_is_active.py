# Generated by Django 4.0 on 2023-07-09 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pills', '0002_alter_pillalarm_periodic_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pillalarm',
            name='is_active',
        ),
    ]