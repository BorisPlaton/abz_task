# Generated by Django 4.0.4 on 2022-05-09 00:32

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_alter_employee_options_alter_employee_employee_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='workers', to='employees.employee', verbose_name='Начальник'),
        ),
    ]