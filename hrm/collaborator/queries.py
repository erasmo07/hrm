import graphene
from graphene_django import DjangoObjectType

from hrm.collaborator import models


class CollaboratorQueries(DjangoObjectType):
    
    class Meta:
        model = models.Collaborator
        fields = '__all__'


class PositionQueries(DjangoObjectType):
    
    class Meta:
        model = models.Position
        fields = '__all__'


class LevelQueries(DjangoObjectType):

    class Meta:
        model = models.Level
        fields = '__all__'



class OrganizationUnitQueries(DjangoObjectType):

    class Meta:
        model = models.OrganizationUnit
        fields = '__all__'