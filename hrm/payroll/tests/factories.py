from factory import DjangoModelFactory, Faker, post_generation

from hrm.payroll import models


class TypePayrollFactory(DjangoModelFactory):

    class Meta:
        model = models.TypePayroll


class LawDiscountFactory(DjangoModelFactory):
    
    class Meta:
        model = models.LawDiscount


class PayrollConfigurationFactory(DjangoModelFactory):
    
    class Meta:
        model = models.PayrollConfiguration