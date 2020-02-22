import graphene
from graphql_jwt.decorators import login_required

from hrm.users.models import Organization
from hrm.payroll import queries


class TypePayrollSchema(graphene.ObjectType):
    type_payrolls = graphene.List(queries.TypePayrollQueries)
    type_payroll = graphene.Field(
        queries.TypePayrollQueries, uuid=graphene.String())
    
    @login_required
    def resolve_type_payrolls(self, info, *args, **kwargs):
        return queries.models.TypePayroll.objects.all()
    
    @login_required
    def resolve_type_payroll(self, info, *args, **kwargs):
        return queries.models.TypePayroll.objects.get(**kwargs)


class LawDiscountSchema(graphene.ObjectType):
    law_discounts = graphene.List(queries.LawDiscountQueries)
    law_discount = graphene.Field(
        queries.LawDiscountQueries, uuid=graphene.String())
    
    @login_required
    def resolve_law_discounts(self, info, *args, **kwargs):
        return queries.models.LawDiscount.objects.all()
    
    @login_required
    def resolve_law_discount(self, info, *args, **kwargs):
        return queries.models.LawDiscount.objects.get(**kwargs)


class PayrollConfigurationSchema(graphene.ObjectType):
    payroll_configuration = graphene.Field(
        queries.PayrollConfigurationQueries,
        organization=graphene.String(required=True))
    
    @login_required
    def resolver_payroll_configuration(self, info, *args, **kwargs):
        user_has_organization = Organization.objects.get()
        return queries.models.PayrollConfiguration(
            organization=kwargs.get('organization'))


class PayrollAppSchema(
    LawDiscountSchema,
    PayrollConfigurationSchema,
    TypePayrollSchema,
    graphene.ObjectType):
    pass