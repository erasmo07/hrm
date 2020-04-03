import graphene
from graphql_jwt.decorators import login_required

from hrm.users.models import Organization
from hrm.payroll import queries, models


class TypePayrollSchema(graphene.ObjectType):
    type_payrolls = graphene.List(queries.TypePayrollQueries)
    type_payroll = graphene.Field(
        queries.TypePayrollQueries, id=graphene.String())
    
    @login_required
    def resolve_type_payrolls(self, info, *args, **kwargs):
        return queries.models.TypePayroll.objects.all()
    
    @login_required
    def resolve_type_payroll(self, info, *args, **kwargs):
        return queries.models.TypePayroll.objects.get(**kwargs)


class LawDiscountSchema(graphene.ObjectType):
    law_discounts = graphene.List(queries.LawDiscountQueries)
    law_discount = graphene.Field(
        queries.LawDiscountQueries, id=graphene.String())
    
    @login_required
    def resolve_law_discounts(self, info, *args, **kwargs):
        return queries.models.LawDiscount.objects.all()
    
    @login_required
    def resolve_law_discount(self, info, *args, **kwargs):
        return queries.models.LawDiscount.objects.get(**kwargs)


class PayrollConfigurationSchema(graphene.ObjectType):
    payroll_configuration = graphene.Field(
        queries.PayrollConfigurationQueries,
        organization=graphene.UUID(required=True))
    
    @login_required
    def resolve_payroll_configuration(self, info, *args, **kwargs):
        return models.PayrollConfiguration.objects.filter(
            **kwargs).first()


class PayrollAppSchema(
    LawDiscountSchema,
    PayrollConfigurationSchema,
    TypePayrollSchema,
    graphene.ObjectType):
    pass