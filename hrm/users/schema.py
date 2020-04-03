import graphene
import graphql_jwt
from graphql_jwt.decorators import permission_required, login_required
from hrm.users import queries


class OrganizatonSchema(graphene.ObjectType):
    organizations = graphene.List(queries.OrganizationQuery)
    organization = graphene.Field(
        queries.OrganizationQuery, user=graphene.UUID())

    @login_required
    @permission_required('users.view_organization')
    def resolve_organizations(self, info, *args, **kwargs):
        return queries.models.Organization.objects.filter(
            user=info.context.user)

    @login_required
    @permission_required('users.view_organization')
    def resolve_organization(self, info, *args, **kwargs):
        return queries.models.Organization.objects.get(**kwargs)


class UserSchema(graphene.ObjectType):
    current_user = graphene.Field(queries.UserQuery)
    users = graphene.List(queries.UserQuery)
    user = graphene.Field(
        queries.UserQuery,
        id=graphene.UUID(),
        email=graphene.String())
    
    def resolve_current_user(self, info, *args, **kwargs):
        return info.context.user

    def resolve_users(self, info, *args, **kwargs):
        return queries.models.User.objects.all()
    
    def resolve_user(self, info, *args, **kwargs):
        return queries.models.User.objects.get(**kwargs)


class UserAppSchema(
    UserSchema,
    OrganizatonSchema,
    graphene.ObjectType):
    pass