from graphene_django import DjangoObjectType

from hrm.users import models


class UserQuery(DjangoObjectType):
    class Meta:
        model = models.User