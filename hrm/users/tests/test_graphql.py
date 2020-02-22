import json

from django.contrib.auth.models import Permission
from django.forms import model_to_dict
from graphene_django.utils.testing import GraphQLTestCase

from config.schema import schema
from graphql_jwt.testcases import JSONWebTokenTestCase
from hrm.users import models
from hrm.users.tests import factories


class UserTestCase(GraphQLTestCase):

    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.model = models.User
        factories.UserFactory()

    def test_can_list_users(self):
        response = self.query(
            '''
            query{
                users {
                    firstName, lastName, email
                }
            }
            ''',
            op_name='users'
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content.get('data').get('users')), 1)
    
    def test_can_detail_user(self):
        user = factories.UserFactory()

        response = self.query(
            '''
            query($uuid: String!){
                user(uuid: $uuid) {
                    uuid
                }
            }
            ''',
            op_name='user',
            variables={'uuid': str(user.uuid)}
        )
        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(content['data']['user']['uuid'], str(user.uuid))
    
    def test_can_create_user_with_same_email(self):
        instance = factories.UserFactory()
        variables = model_to_dict(
            instance=instance,
            fields=['first_name', 'last_name', 'email', 'password'])
        response = self.query(
            '''
            mutation(
                $email: String!,
                $first_name: String!,
                $last_name: String!,
                $password: String!){
                    createUser(
                        email: $email,
                        firstName: $first_name,
                        lastName: $last_name,
                        password: $password
                    ){ errorMessage, ok }
            }
            ''',
            op_name='createUser', variables=variables)

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        error_message = content['data']['createUser']['errorMessage']
        ok = content['data']['createUser']['ok']

        self.assertFalse(ok)
        self.assertEqual('Este correo ya existe', error_message)
    
    def test_can_create_user(self):
        
        instance = factories.UserFactory()
        variables = model_to_dict(
            instance=instance,
            fields=['first_name', 'last_name', 'email', 'password'])
        instance.delete()

        response = self.query(
            '''
            mutation(
                $email: String!,
                $first_name: String!,
                $last_name: String!,
                $password: String!){
                    createUser(
                        email: $email,
                        firstName: $first_name,
                        lastName: $last_name,
                        password: $password
                    ){ ok, user{ uuid }}
            }
            ''',
            op_name='createUser', variables=variables)

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        uuid = content['data']['createUser']['user']['uuid']
        ok = content['data']['createUser']['ok']

        self.assertTrue(ok)
        self.assertTrue(self.model.objects.filter(uuid=uuid).exists())

        user = models.User.objects.get(uuid=uuid)
        assert user.user_permissions.count() == Permission.objects.count()


class OrganizationTestCase(GraphQLTestCase, JSONWebTokenTestCase):
    
    GRAPHQL_SCHEMA = schema

    def test_list_organization(self):
        user = factories.UserFactory()
        
        user.set_password('@1234567')
        user.save()

        organization = factories.OrganizationFactory(user=user)

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
                'username': user.username, 'password': '@1234567'}
        )

        self.assertResponseNoErrors(response_token)
        token = json.loads(response_token.content)['data']['tokenAuth']['token']

        response_organization = self.query(
            '''
            query{ organizations{ name } }
            ''',
            op_name='organizations',
            headers={"HTTP_AUTHORIZATION": 'JWT %s' % token}
        )

        self.assertResponseNoErrors(response_organization)
        data = json.loads(response_organization.content)['data']

        organization_name = data.get('organizations')[0]['name']
        self.assertEqual(organization_name, organization.name)
