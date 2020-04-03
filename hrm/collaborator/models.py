from hrm.contrib.models import BaseModel, Status
from hrm.contrib.enums import StatusEnums
from django.db import models


class Level(BaseModel):
    name = models.CharField('Nivel', max_length=50)
    organization = models.ForeignKey(
        'users.Organization', on_delete=models.CASCADE)


class PersonalArea(BaseModel):
    name = models.CharField("Area de personal", max_length=50)
    organization = models.ForeignKey(
        'users.Organization', on_delete=models.CASCADE)


class OrganizationUnit(BaseModel):
    name = models.CharField('Organization Unit', max_length=100)
    organization = models.ForeignKey(
        'users.Organization', on_delete=models.CASCADE)


class Position(BaseModel):
    name = models.CharField('Posicion', max_length=50)
    salary = models.DecimalField(
        'Base salary', max_digits=5, decimal_places=2)

    organization = models.ForeignKey(
        'users.Organization', on_delete=models.CASCADE)
    organization_unit = models.ForeignKey(
        "collaborator.OrganizationUnit",
        on_delete=models.CASCADE)
    level = models.ForeignKey(
        'collaborator.Level', on_delete=models.CASCADE)


class StatusCollaborator(Status):
    pass


class Collaborator(BaseModel):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=64)
    date_admission = models.DateField()

    identification_number = models.CharField(
        'Identification Number', max_length=11)

    user = models.OneToOneField(
        'users.User', on_delete=models.CASCADE,
        blank=True, null=True)
    organization = models.ForeignKey(
        'users.Organization', on_delete=models.CASCADE)

    position = models.ForeignKey(
        'collaborator.Position', on_delete=models.CASCADE)

    status = models.ForeignKey(
        'collaborator.StatusCollaborator',
        on_delete=models.CASCADE,
        limit_choices_to=StatusEnums.collaborator.limit_choices_to)

    image = models.ImageField(
        upload_to='colaborador', blank=True, null=True)
