import graphene
from graphene_django import DjangoObjectType

from hrm.payroll import models


class TypePayrollQueries(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = models.TypePayroll
        exclude = ['id']
        interfaces = (graphene.relay.Node, )


class LawDiscountQueries(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = models.LawDiscount
        exclude = ['id']
        interfaces = (graphene.relay.Node, )


class PayrollConfigurationQueries(DjangoObjectType):

    class Meta:
        model = models.PayrollConfiguration
        exclude = ['id']
        interfaces = (graphene.relay.Node, )