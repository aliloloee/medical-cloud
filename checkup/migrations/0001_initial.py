# Generated by Django 4.0 on 2023-07-10 10:18

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
            name='BloodTest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'STANDARD'), (2, 'PRO'), (3, 'ADVANCED')], default=1, verbose_name='Gender')),
                ('title', models.CharField(max_length=100, verbose_name='Blood test title')),
                ('description', models.CharField(blank=True, max_length=300, verbose_name='blood test description')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_tests', to='accounts.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Blood test',
                'verbose_name_plural': 'Blood tests',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='BloodTestResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.PositiveIntegerField(choices=[(1, 'CBC'), (2, 'ESR'), (3, 'FBS'), (4, 'TG'), (5, 'CHO'), (6, 'BUN'), (7, 'CREA'), (8, 'SGOT'), (9, 'URIC_ACID'), (10, 'SGPT'), (11, 'ALP'), (12, 'BILI_T'), (13, 'BILI_D'), (14, 'T_PROTEIN'), (15, 'ALB'), (16, 'MG'), (17, 'ZINC'), (18, 'VIT_D'), (19, 'IRON'), (20, 'TIBC'), (21, 'TSH'), (22, 'T4'), (23, 'T3'), (24, 'CA'), (25, 'PHO'), (26, 'NA'), (27, 'K'), (28, 'UA'), (29, 'UC')], verbose_name='Result name')),
                ('value', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='Result value')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('blood_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_test_results', to='checkup.bloodtest', verbose_name='Blood test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_test_results', to='accounts.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Blood test result',
                'verbose_name_plural': 'Blood test results',
                'ordering': ('created',),
            },
        ),
    ]