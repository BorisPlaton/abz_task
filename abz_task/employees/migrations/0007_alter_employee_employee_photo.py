# Generated by Django 4.0.4 on 2022-05-05 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_employee_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_photo',
            field=models.ImageField(default='photo/default.png', upload_to='', verbose_name='Фото работника'),
        ),
    ]
