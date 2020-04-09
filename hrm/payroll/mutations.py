import graphene
from django.db.utils import IntegrityError

from graphql_jwt.decorators import login_required
from graphql_jwt.exceptions import PermissionDenied
from hrm.users.models import Organization
from hrm.users.queries import OrganizationQuery

from . import models, queries, tasks


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

        if not create:
            return CreatePayrollConfiguration(
                ok=True, configuration=configuration)

        for law_discount in models.LawDiscount.objects.all():
            models.LawDiscountOrganization.objects.create(
                law_discount=law_discount,
                organization_id=kwargs.get('organization'))

        for discount in kwargs.get('discounts', []):
            models.Discount.objects.create(
                organization_id=kwargs.get("organization"),
                **discount)

        for additional in kwargs.get('additionals', []):
            models.Additional.objects.create(
                organization_id=kwargs.get("organization"),
                **additional)
        
        tasks.CreatePayroll().delay(configuration.id)

        return CreatePayrollConfiguration(ok=True, configuration=configuration)


class PayrollMutation(graphene.ObjectType):
    create_payroll_configuration = CreatePayrollConfiguration.Field()
