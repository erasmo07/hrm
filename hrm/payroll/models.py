from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrm.contrib.models import BaseModel, Status
from hrm.contrib import enums


class TypePayroll(BaseModel):
    name = models.CharField(
        _("Tipo de nomina"), max_length=50,
        choices=[(
            enums.TypePayrollEnums.biweekly,
            enums.TypePayrollEnums.biweekly)])
    count_mount = models.IntegerField('Count on Month', default=2)


class LawDiscount(BaseModel):
    name = models.CharField(_("Nombre"), max_length=50)
    porcentage = models.DecimalField(
        _("Porcentaje"), max_digits=5, decimal_places=2)


class LawDiscountOrganization(BaseModel):
    law_discount = models.ForeignKey(
        "payroll.LawDiscount", on_delete=models.CASCADE)
    organization = models.ForeignKey(
        "users.Organization",
        related_name='law_discounts',
        on_delete=models.CASCADE)


class Discount(BaseModel):
    organization = models.ForeignKey(
        "users.Organization",
        related_name='discounts',
        on_delete=models.CASCADE)
    name = models.CharField(_("Adicionales"), max_length=50)
    porcentage = models.DecimalField(
        _("Porcentaje"), max_digits=5, decimal_places=2)


class Additional(BaseModel):
    organization = models.ForeignKey(
        "users.Organization",
        related_name='additionals',
        on_delete=models.CASCADE)
    name = models.CharField(_("Adicionales"), max_length=50)
    porcentage = models.DecimalField(
        _("Porcentaje"), max_digits=5, decimal_places=2)


class PayrollConfiguration(BaseModel):
    active_month = models.IntegerField(
        "Active Months", default=6)
    organization = models.OneToOneField(
        "users.Organization",
        related_name='payroll_configuration',
        on_delete=models.CASCADE)
    type_payroll = models.ForeignKey(
        "payroll.TypePayroll",
        related_name='type', on_delete=models.CASCADE)


class StatusPayroll(Status):
    pass


class Payroll(BaseModel):
    date_apply = models.DateField('Date to apply')

    status = models.ForeignKey(
        "payroll.StatusPayroll",
        on_delete=models.CASCADE)
    configuration = models.ForeignKey(
        "payroll.PayrollConfiguration",
        on_delete=models.CASCADE)
    period = models.ForeignKey(
        "payroll.Period", on_delete=models.CASCADE)


class PayrollCollaborator(BaseModel):
    payroll = models.ForeignKey(
        "payroll.Payroll", on_delete=models.CASCADE)
    collaborator = models.ForeignKey(
        "collaborator.Collaborator",
        related_name='payroll',
        on_delete=models.CASCADE)
    discounts = models.ManyToManyField("payroll.Discount")
    additionals = models.ManyToManyField("payroll.Additional")
    law_discounts = models.ManyToManyField("payroll.LawDiscountOrganization")


class Period(BaseModel):
    order = models.IntegerField("Count")
    day_apply = models.IntegerField(_("Day to apply periods"))