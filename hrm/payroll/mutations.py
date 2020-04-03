import graphene
from django.db.utils import IntegrityError

from graphql_jwt.decorators import login_required
from graphql_jwt.exceptions import PermissionDenied
from hrm.users.models import Organization
from hrm.users.queries import OrganizationQuery

from . import models, queries


class DiscountInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    porcentage = graphene.Int(required=True)


class AdditionalInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    porcentage = graphene.Int(required=True)


class CreatePayrollConfiguration(graphene.Mutation):

    class Arguments:
        organization = graphene.UUID(required=True)
        type_payroll = graphene.UUID(required=True)

        discounts = graphene.List(DiscountInput)
        additionals = graphene.List(AdditionalInput)

    ok = graphene.Boolean()
    errors = graphene.String()
    configuration = graphene.Field(queries.PayrollConfigurationQueries)

    @login_required
    def mutate(self, info, *args, **kwargs):
        if not info.context.user.organization_set.filter(
                id=kwargs.get('organization')).exists():
            message = 'No tiene esta organizacion'
            raise PermissionDenied(message=message)

        configuration, create = models.PayrollConfiguration.objects.get_or_create(
            organization_id=kwargs.get('organization'),
            type_payroll_id=kwargs.get('type_payroll')
        )

        if create:
            return CreatePayrollConfiguration(
                ok=True, configuration=configuration)

        lay_discount = models.LawDiscount.objects.all()
        configuration.law_discounts.add(*lay_discount)

        if 'discounts' in kwargs:
            discounts = map(
                lambda x: models.Discount.objects.create(
                    organization_id=kwargs.get("organization"), **x),
                kwargs.get('discounts'))
            configuration.discounts.add(*discounts)
        
        if 'additionals' in kwargs:
            additionals = map(
                lambda x: models.Additional.objects.create(
                    organization=kwargs.get("organization"), **x),
                kwargs.get('additionals'))
            configuration.additionals.add(*additionals)

        return CreatePayrollConfiguration(ok=True, configuration=configuration)


class PayrollMutation(graphene.ObjectType):
    create_payroll_configuration = CreatePayrollConfiguration.Field()
