from factory import DjangoModelFactory, Faker, post_generation

from hrm.contrib import enums
from hrm.payroll import models


class TypePayrollFactory(DjangoModelFactory):
    name = enums.TypePayrollEnums.biweekly

    class Meta:
        model = models.TypePayroll


class LawDiscountFactory(DjangoModelFactory):
    
    class Meta:
        model = models.LawDiscount


class LawDiscountOrganizationFactory(DjangoModelFactory):
    
    class Meta:
        model = models.LawDiscountOrganization


class PayrollConfigurationFactory(DjangoModelFactory):
    
    class Meta:
        model = models.PayrollConfiguration


class PeriodFactory(DjangoModelFactory):

    class Meta:
        model = models.Period