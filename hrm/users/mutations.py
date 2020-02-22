import graphene
from django.db.utils import IntegrityError
from django.contrib.auth.models import Permission
from . import models, queries


class CreateUser(graphene.Mutation):

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    ok = graphene.Boolean()
    error_message = graphene.String()

    user = graphene.Field(queries.UserQuery)

    def mutate(self, info, *args, **kwargs):
        try:
            password = kwargs.pop('password')

            kwargs['username'] = kwargs.get('email')
            user = models.User.objects.create(**kwargs)

            user.set_password(password)
            user.save()

            # Assign all permitions
            user.user_permissions.set(Permission.objects.all())

            return CreateUser(user=user, ok=True)
        except IntegrityError as exception:
            message = 'Este correo ya existe'
            return CreateUser(ok=False, error_message=message) 


class CreateOrganization(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        principal_email = graphene.String(required=True)

    ok = graphene.Boolean()
    error_message = graphene.String()

    organization = graphene.Field(queries.OrganizationQuery)

    def mutate(self, info, *args, **kwargs):
        organization = models.Organization.objects.create(
            user=info.context.user, **kwargs)
        return CreateOrganization(organization=organization, ok=True)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_organization = CreateOrganization.Field()