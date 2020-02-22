# Generated by Django 2.2.4 on 2020-02-22 14:24

from django.db import migrations
from hrm.contrib import enums


def create_type_payroll(apps, schema_editor):
    type_payroll = apps.get_model('payroll', 'TypePayroll')
    type_payroll.objects.get_or_create(name=enums.TypePayrollEnums.biweekly)


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0007_auto_20200212_1450'),
    ]

    operations = [
        migrations.RunPython(create_type_payroll),
    ]