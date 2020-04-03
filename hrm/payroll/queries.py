import graphene
from graphene_django import DjangoObjectType

from hrm.payroll import models


class TypePayrollQueries(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = models.TypePayroll
        fields = "__all__"


class LawDiscountQueries(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = models.LawDiscount
        fields = "__all__"


class PayrollConfigurationQueries(DjangoObjectType):

    class Meta:
        model = models.PayrollConfiguration
        fields = "__all__"