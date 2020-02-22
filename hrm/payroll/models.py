from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrm.contrib.models import BaseModel
from hrm.contrib import enums


class TypePayroll(BaseModel):
    name = models.CharField(
        _("Tipo de nomina"), max_length=50,
        choices=[(
            enums.TypePayrollEnums.biweekly,
            enums.TypePayrollEnums.biweekly)])


class LawDiscount(BaseModel):
    name = models.CharField(_("Nombre"), max_length=50)
    porcentage = models.DecimalField(
        _("Porcentaje"), max_digits=5, decimal_places=2)


class Discount(BaseModel):
    organization = models.OneToOneField(
        "users.Organization",
        related_name='discounts',
        on_delete=models.CASCADE)
    name = models.CharField(_("Adicionales"), max_length=50)
    porcentage = models.DecimalField(
        _("Porcentaje"), max_digits=5, decimal_places=2)


class Additional(BaseModel):
    organization = models.OneToOneField(
        "users.Organization",
        related_name='additionals',
        on_delete=models.CASCADE)
    name = models.CharField(_("Adicionales"), max_length=50)
    porcentage = models.DecimalField(
        _("Porcentaje"), max_digits=5, decimal_places=2)


class PayrollConfiguration(BaseModel):
    type_payroll = models.ForeignKey(
        "payroll.TypePayroll",
        related_name='type', on_delete=models.CASCADE)
    organization = models.OneToOneField(
        "users.Organization",
        related_name='payroll_configuration', on_delete=models.CASCADE)
    law_discounts = models.ManyToManyField(
        "payroll.LawDiscount", related_name='law_discounts')
    discounts = models.ManyToManyField(
        "payroll.Discount", related_name='discounts')
    additionals = models.ManyToManyField(
        "payroll.Additional", related_name='additionals')
