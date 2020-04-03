import graphene

from graphql_jwt.decorators import permission_required, login_required
from hrm.users.models import Organization
from hrm.users.queries import OrganizationQuery

from . import models, queries, enums



class CreateCollaborator(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        date_admission = graphene.Date(required=True)

        position_id = graphene.UUID(required=True)
        organization_id = graphene.UUID(required=True)


    ok = graphene.Boolean()
    errors = graphene.String()
    collaborator = graphene.Field(queries.CollaboratorQueries)
    organization = graphene.Field(OrganizationQuery)
    position = graphene.Field(queries.PositionQueries)

    @login_required
    @permission_required('collaborator.add_collaborator')
    def mutate(self, info, *args, **kwargs):
        status_active, _ = models.StatusCollaborator.objects.get_or_create(
            name=enums.StatusCollaboratorEnums.active)

        collaborator = models.Collaborator.objects.create(
            status=status_active, **kwargs)
        return CreateCollaborator(
            ok=True, collaborator=collaborator)


class CreateLevel(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
        organization_id = graphene.UUID(required=True)
    
    ok = graphene.Boolean()
    level = graphene.Field(queries.LevelQueries)

    @login_required
    @permission_required('collaborator.add_level')
    def mutate(self, info, *args, **kwargs):
        level = models.Level.objects.create(
            **kwargs
        )

        return CreateLevel(ok=True, level=level)


class CreateOrganizationUnit(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
        organization_id = graphene.UUID(required=True)
    
    ok = graphene.Boolean()
    organization_unit = graphene.Field(
        queries.OrganizationUnitQueries)

    @login_required
    # @permission_required('collaborator.add_organization_unit')
    def mutate(self, info, *args, **kwargs):
        organization_unit = models.OrganizationUnit.objects.create(**kwargs)
        return CreateOrganizationUnit(
            ok=True,
            organization_unit=organization_unit)


class CreatePosition(graphene.Mutation):
    
    class Arguments:
        name = graphene.String(required=True)
        organization_id = graphene.UUID(required=True)
        level_id = graphene.UUID(required=True)
        organization_unit_id = graphene.UUID(required=True)
        salary = graphene.String(required=True)
    
    ok = graphene.Boolean()
    position = graphene.Field(queries.PositionQueries)

    @login_required
    @permission_required('collaborator.add_position')
    def mutate(self, info, *args, **kwargs):
        position = models.Position.objects.create(**kwargs)
        return CreatePosition(ok=True, position=position)



class CollaboratorMutation(graphene.ObjectType):
    create_collaborator = CreateCollaborator.Field()
    create_level = CreateLevel.Field()
    create_organization_unit = CreateOrganizationUnit.Field()
    create_position = CreatePosition.Field()