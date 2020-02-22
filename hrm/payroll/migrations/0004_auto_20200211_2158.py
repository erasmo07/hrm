# Generated by Django 2.2.4 on 2020-02-11 21:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200207_0447'),
        ('payroll', '0003_auto_20200211_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Additional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=120)),
                ('name', models.CharField(max_length=50, verbose_name='Adicionales')),
                ('porcentage', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Porcentaje')),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='additionals', to='users.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=120)),
                ('law', models.BooleanField(verbose_name='Por ley')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('porcentage', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Porcentaje')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='typepayroll',
            name='name',
            field=models.CharField(choices=[('Quincenal', 'Quincenal')], max_length=50, verbose_name='Tipo de nomina'),
        ),
        migrations.CreateModel(
            name='PayrollConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=120)),
                ('additionals', models.ManyToManyField(related_name='additionals', to='payroll.Additional')),
                ('discounts', models.ManyToManyField(related_name='discounts', to='payroll.Discount')),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payroll_configuration', to='users.Organization')),
                ('type_payroll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type', to='payroll.TypePayroll')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]