# Generated by Django 2.2.4 on 2020-02-11 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typepayroll',
            name='name',
            field=models.CharField(choices=[('Quincena', 'Quincenal')], max_length=50),
        ),
    ]