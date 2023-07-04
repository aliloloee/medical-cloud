# Generated by Django 4.0 on 2023-06-26 14:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'STANDARD'), (2, 'PRO'), (3, 'ADVANCED'), (4, 'FREE')], default=1, verbose_name='Type')),
                ('charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=11, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Charge')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='CustomProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Age')),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'STANDARD'), (2, 'PRO'), (3, 'ADVANCED')], default=1, verbose_name='Gender')),
                ('education', models.PositiveSmallIntegerField(choices=[(1, 'BELOW HIGHSCHOOL'), (2, 'HIGHSCHOOL'), (3, 'ABOVE HIGHSCHOOL')], default=1, verbose_name='Education Level')),
                ('employment', models.PositiveSmallIntegerField(choices=[(1, 'UNEMPLOYED'), (2, 'EMPLOYED'), (3, 'RETIRED')], default=1, verbose_name='Employment status')),
                ('tobacco', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Tobacco Usage')),
                ('alcohol', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Alcohol consumption')),
                ('physical_activity', models.SmallIntegerField(choices=[(0, 'NEVER'), (1, 'SELDOM'), (2, 'REGULAR')], default=0, verbose_name='Physical activity')),
                ('fruit_consumption', models.PositiveSmallIntegerField(choices=[(0, 'LOW'), (1, 'AVERAGE'), (2, 'HIGH')], default=0, verbose_name='Fruit consumption')),
                ('vegetable_consumption', models.PositiveSmallIntegerField(choices=[(0, 'LOW'), (1, 'AVERAGE'), (2, 'HIGH')], default=0, verbose_name='Vegetable consumption')),
                ('meat_consumption', models.PositiveSmallIntegerField(choices=[(0, 'LOW'), (1, 'AVERAGE'), (2, 'HIGH')], default=0, verbose_name='Meat consumption')),
                ('obesity', models.PositiveSmallIntegerField(choices=[(1, 'THIN'), (2, 'FIT'), (3, 'OVERWEIGHT'), (4, 'EXTREME OVERWEIGHT')], default=1, verbose_name='Obesity')),
                ('sedentary_job', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Sedentary job')),
                ('diabetes_history', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Diabetes history')),
                ('cholesterol_history', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Cholesterol history')),
                ('blood_pressure_history_on_mother_side', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Blood pressure history from mother side')),
                ('blood_pressure_history_on_father_side', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Blood pressure history from father side')),
                ('salty_diet', models.SmallIntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='Salty diet')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='custom_profile', to='accounts.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Custom Profile',
                'verbose_name_plural': 'Custom Profiles',
                'ordering': ('created',),
            },
        ),
    ]
