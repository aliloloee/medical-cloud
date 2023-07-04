# Generated by Django 4.0 on 2023-06-22 08:23

import devices.utils
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('api_key', models.CharField(blank=True, default=devices.utils.generate_api_key, max_length=100, verbose_name='API Key')),
                ('name', models.CharField(max_length=100, verbose_name='Device name')),
                ('description', models.CharField(blank=True, max_length=300, verbose_name='Device description')),
                ('serial_number', models.CharField(max_length=100, unique=True, verbose_name='Device serial')),
                ('is_active', models.BooleanField(default=False, verbose_name='Device is active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='accounts.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
                'ordering': ('created',),
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Record name')),
                ('data', models.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='devices.device', verbose_name='Device')),
            ],
            options={
                'verbose_name': 'Record',
                'verbose_name_plural': 'Records',
                'ordering': ('created',),
            },
        ),
    ]