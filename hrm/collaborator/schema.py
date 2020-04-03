import graphene
from graphql_jwt.decorators import login_required

from hrm.collaborator import queries, models


class CollabroatorSchema(graphene.ObjectType):
    collaborators = graphene.Field(
        lambda: graphene.List(queries.CollaboratorQueries),
        organization=graphene.UUID(required=True))
    collaborator = graphene.Field(
        queries.CollaboratorQueries
    )

    @login_required
    def resolve_collaborators(self, info, *args, **kwargs):
        return models.Collaborator.objects.filter(**kwargs)


class PositionSchema(graphene.ObjectType):
    positions = graphene.Field(
        lambda: graphene.List(queries.PositionQueries),
        organization=graphene.UUID(required=True)
    )

    @login_required
    def resolve_positions(self, info, *args, **kwargs):
        return models.Position.objects.filter(**kwargs)


class LevelSchema(graphene.ObjectType):
    levels = graphene.Field(
        lambda: graphene.List(queries.LevelQueries),
        organization=graphene.UUID(required=True)
    )

    @login_required
    def resolve_levels(self, info, *args, **kwargs):
        return models.Level.objects.filter(**kwargs)


class OrganizationUnitSchema(graphene.ObjectType):
    organization_units = graphene.Field(
        lambda: graphene.List(
            queries.OrganizationUnitQueries),
        organization=graphene.UUID(required=True)
    )

    @login_required
    def resolve_organization_units(self, info, *args, **kwargs):
        return models.OrganizationUnit.objects.filter(**kwargs)


class CollaboratorAppSchema(
    LevelSchema,
    OrganizationUnitSchema,
    PositionSchema,
    CollabroatorSchema,
    graphene.ObjectType):
    pass