import json

from config.schema import schema
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.forms import model_to_dict
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from rest_framework.authtoken.models import Token

from hrm.collaborator import models
from hrm.collaborator.tests import factories
from hrm.users.tests.factories import OrganizationFactory, UserFactory


class CollaboratorTestCase(GraphQLTestCase, JSONWebTokenTestCase):
    
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = UserFactory()
        
        self.organization = OrganizationFactory.create(user=self.user)

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
    
    def test_can_query_collaborators(self):
        # GIVEN
        factories.CollaboratorFactory.create(
            organization=self.organization
        )
    
        # WHEN
        response = self.query(
            '''
            query($organization: UUID!){
                collaborators(organization: $organization){
                    id, name, lastName
                }
            }
            ''',
            op_name='collaborators',
            variables={'organization': str(self.organization.id)},
            headers={"HTTP_AUTHORIZATION": 'JWT %s' % self.token}
        )

        # THEN
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(
            len(content.get('data').get('collaborators')), 1)
        
    def test_can_create_collaborator(self):
        # GIVEN
        collaborator = factories.CollaboratorFactory.create(
            organization=self.organization
        )

        # WHEN
        variables = model_to_dict(
            collaborator,
            fields=[
                'date_admission', 'last_name',
                'name', 'organization', 'position'])
        variables.update(dict(
            organization=str(collaborator.organization.id),
            position=str(collaborator.position.id)))

        response = self.query(
            '''
            mutation(
                $date_admission: Date!,
                $last_name: String!,
                $name: String!,
                $organization: UUID!,
                $position: UUID!,
            ){
                createCollaborator(
                    dateAdmission: $date_admission,
                    lastName: $last_name,
                    name: $name,
                    organizationId: $organization,
                    positionId: $position,
                ){
                    collaborator {
                        id, name, lastName,
                        organization { id },
                        position { id },
                    }
                }
            }
            ''',
            op_name='createCollaborator',
            variables=variables,
            headers={"HTTP_AUTHORIZATION": 'JWT %s' % self.token}
        )
        
        # THEN
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        body = content.get('data').get('createCollaborator')
        self.assertIn('id', body['collaborator'])
        self.assertIn('name', body['collaborator'])
        self.assertIn('lastName', body['collaborator'])

        self.assertEqual(
            str(self.organization.id),
            body['collaborator']['organization']['id'])
        self.assertEqual(
            str(collaborator.position.id),
            body['collaborator']['position']['id'])


class TestLevelQueries(TestCase):
    
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = UserFactory()
        
        self.organization = OrganizationFactory.create(user=self.user)
    
    def test_can_query_levels(self):
        # GIVEN
        factories.LevelFactory.create(
            organization=self.organization
        )
    
        # WHEN
        response = self.query(
            '''
            query($organization: UUID!){
                levels(organization: $organization){
                    id, name, lastName
                }
            }
            ''',
            variables={'organization': str(self.organization.id)},
            headers={"HTTP_AUTHORIZATION": 'JWT %s' % self.token}
        )

        # THEN
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(
            len(content.get('data').get('collaborators')), 1)