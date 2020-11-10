import graphene
import calendar
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


class PayrollQueries(DjangoObjectType):

    class Meta:
        model = models.Payroll
        fields = '__all__'
    
    month_label = graphene.String()

    def resolve_month_label(self, info):
        return calendar.month_name[self.date_apply.month]


class PayrollCollaborator(DjangoObjectType):

    class Meta:
        model = models.PayrollCollaborator
        fields = '__all__'


class PeriodQueries(DjangoObjectType):

    class Meta:
        model = models.Period
        fields = "__all__"


class StatusPayrollQueries(DjangoObjectType):

    class Meta:
        model = models.StatusPayroll
        fields = '__all__'