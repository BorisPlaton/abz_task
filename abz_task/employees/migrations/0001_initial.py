# Generated by Django 4.0.4 on 2022-05-01 23:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=32, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=32, verbose_name='Отчество')),
                ('date_employment', models.DateTimeField(verbose_name='Дата трудоустройства')),
                ('payment', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Заработная плата не может быть меньше нуля.')], verbose_name='Зарплата')),
                ('boss', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='employees.employee', verbose_name='Начальник')),
                ('position', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='employees.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Работник',
                'verbose_name_plural': 'Работники',
            },
        ),
    ]
