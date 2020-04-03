import json

from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

from config.schema import schema
from hrm.users.tests.factories import OrganizationFactory, UserFactory


class TestCase(GraphQLTestCase, JSONWebTokenTestCase):
    
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = UserFactory()
        
        self.organization = OrganizationFactory.create(
            user=self.user)

    @property
    def token(self):
        response_token = self.query(
            '''
            mutation($username: String!, $password: String!){
                tokenAuth(username: $username, password: $password) {
                    token
                }
            }
            ''',
            op_name='tokenAuth',
            variables={
                'username': self.user.username, 'password': '@1234567'}
        )

        self.assertResponseNoErrors(response_token)
        return json.loads(
            response_token.content
        )['data']['tokenAuth']['token']