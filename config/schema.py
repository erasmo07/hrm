import graphene
from hrm.users import queries as user_queries

class Query(graphene.ObjectType):
    users = graphene.List(user_queries.UserQuery)

    def resolve_users(self, info):
        return user_queries.models.User.objects.all()

schema = graphene.Schema(query=Query)