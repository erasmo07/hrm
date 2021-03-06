# Generated by Django 2.2.4 on 2020-04-03 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collaborator', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='position',
            name='organization_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collaborator.OrganizationUnit'),
        ),
        migrations.AddField(
            model_name='personalarea',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='organizationunit',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='level',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collaborator.Position'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='status',
            field=models.ForeignKey(limit_choices_to=models.Q(('name', 'Activo'), ('name', 'Dado de baja'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='collaborator.StatusCollaborator'),
        ),
        migrations.AddField(
            model_name='collaborator',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
