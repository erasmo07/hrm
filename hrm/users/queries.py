from graphene import relay 
from graphene_django import DjangoObjectType

from hrm.users import models


class UserQuery(DjangoObjectType):
    class Meta:
        model = models.User
        filter_fields = {
            'email': ['exact'],
            'uuid': ['exact']}

        exclude = ['password', 'id'] 
        interfaces = (relay.Node, )


class OrganizationQuery(DjangoObjectType):
    class Meta:
        model = models.Organization
        filter_fields = {'user': ['exact']}
        fields = '__all__'
        interfaces = (relay.Node, )
