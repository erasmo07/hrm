# Generated by Django 2.2.4 on 2020-02-12 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0006_auto_20200212_1054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payrollconfiguration',
            old_name='discount',
            new_name='discounts',
        ),
    ]
