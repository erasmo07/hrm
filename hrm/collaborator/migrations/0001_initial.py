# Generated by Django 2.2.4 on 2020-03-23 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Nivel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Organization Unit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonalArea',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Area de personal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StatusCollaborator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Status')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Posicion')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='collaborator.Level')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization')),
                ('organization_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collaborator.OrganizationUnit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=64)),
                ('date_admission', models.DateField()),
                ('identification_number', models.CharField(max_length=11, verbose_name='Identification Number')),
                ('image', models.ImageField(blank=True, null=True, upload_to='colaborador')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='collaborator.Position')),
                ('status', models.ForeignKey(limit_choices_to=models.Q(('name', 'Activo'), ('name', 'Dado de baja'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='collaborator.StatusCollaborator')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]