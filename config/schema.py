import graphene
import graphql_jwt
from hrm.users import schema as users_schema, mutations as users_mutations
from hrm.payroll import schema as payroll_schema, mutations as payroll_mutations


class Mutation(
    users_mutations.UserMutation,
    payroll_mutations.PayrollMutation,
    graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(
        payroll_schema.PayrollAppSchema,
        users_schema.UserAppSchema,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)