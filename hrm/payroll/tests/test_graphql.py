import json

from config.schema import schema
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.forms import model_to_dict
from graphene_django.utils.testing import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from rest_framework.authtoken.models import Token

from hrm.payroll import models
from hrm.payroll.tests import factories
from hrm.users.tests.factories import OrganizationFactory, UserFactory


class TypePayrollTestCase(GraphQLTestCase, JSONWebTokenTestCase):

    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = UserFactory()

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
        return json.loads(response_token.content)['data']['tokenAuth']['token']

    def test_can_query_payroll_configuraton(self):
        # GIVEN
        type_payroll = factories.TypePayrollFactory(name='Quincenal')
        organization = OrganizationFactory(user=self.user)
        factories.PayrollConfigurationFactory(
            organization=organization, type_payroll=type_payroll)
    
        # WHEN
        response = self.query(
            """
            query($organization: String!){
                payrollConfiguration(organization: $organization){ uuid }
            }
            """,
            variables={'organization': str(organization.uuid)},
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'}
        )
    
        # THEN
        self.assertResponseNoErrors(response)
        
    
    def test_can_query_type_payroll(self):
        # GIVEN
        factories.TypePayrollFactory(name='Quincenal')

        # WHEN
        response = self.query(
            '''
            query{
                typePayrolls {
                    name
                }
            } 
            ''',
            op_name='typePayrolls',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'}
        )

        # THEN
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content.get('data').get('typePayrolls')), 1)

    def test_can_query_law_discounts(self):
        # GIVEN
        AFP = factories.LawDiscountFactory(name='AFP', porcentage=3.36)

        # WHEN
        response_discount = self.query(
            """
            query{
                lawDiscounts{
                    name, porcentage
                }
            }
            """,
            op_name='lawDiscounts',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'}
        )

        # THEN
        self.assertResponseNoErrors(response_discount)
        content_discount = json.loads(response_discount.content)
    
    def test_user_hasnt_organization(self):
        # GIVEN
        type_payroll = factories.TypePayrollFactory()

        AFP = factories.LawDiscountFactory(name='AFP', porcentage=3.26)
        ARS = factories.LawDiscountFactory(name='ARS', porcentage=2.26)

        organization = OrganizationFactory(user=UserFactory())

        # WHEN
        response = self.query(
            """
            mutation create(
                $typePayroll: String!,
                $organization: String!
            ){
                createPayrollConfiguration(
                    typePayroll: $typePayroll,
                    organization: $organization

                ){
                    ok, errors
                }
            }
            """,
            op_name='createPayrollConfiguration',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            variables = {
                'typePayroll': str(type_payroll.uuid),
                'organization': str(organization.uuid)
            }
        )

        # THEN
        self.assertResponseHasErrors(response)
        content = json.loads(response.content)

        self.assertEqual(
            content.get('errors')[0].get('message'),
            'No tiene esta organizacion')
    
    def test_not_duplicate_configuration(self):
        # GIVEN
        type_payroll = factories.TypePayrollFactory()

        AFP = factories.LawDiscountFactory(name='AFP', porcentage=3.26)
        ARS = factories.LawDiscountFactory(name='ARS', porcentage=2.26)

        organization = OrganizationFactory(user=self.user)
        configuration = factories.PayrollConfigurationFactory(
            organization=organization, type_payroll=type_payroll)

        # WHEN
        response = self.query(
            """
            mutation create(
                $typePayroll: String!,
                $organization: String!
            ){
                createPayrollConfiguration(
                    typePayroll: $typePayroll,
                    organization: $organization

                ){
                    ok, errors
                }
            }
            """,
            op_name='createPayrollConfiguration',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            variables = {
                'typePayroll': str(type_payroll.uuid),
                'organization': str(organization.uuid)
            }
        )

        self.assertResponseNoErrors(response)
        configuration = models.PayrollConfiguration.objects.filter(
            organization__uuid=organization.uuid,
            type_payroll__uuid=type_payroll.uuid
        )
        self.assertEqual(configuration.count(), 1)

    def test_can_create_configuration(self):
        # GIVEN
        type_payroll = factories.TypePayrollFactory()

        AFP = factories.LawDiscountFactory(name='AFP', porcentage=3.26)
        ARS = factories.LawDiscountFactory(name='ARS', porcentage=2.26)

        organization = OrganizationFactory(user=self.user)

        # WHEN
        response = self.query(
            """
            mutation create(
                $typePayroll: String!,
                $organization: String!
            ){
                createPayrollConfiguration(
                    typePayroll: $typePayroll,
                    organization: $organization

                ){
                    ok, errors
                }
            }
            """,
            op_name='createPayrollConfiguration',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            variables = {
                'typePayroll': str(type_payroll.uuid),
                'organization': str(organization.uuid)
            }
        )
        # THEN
        self.assertResponseNoErrors(response)
        content_discount = json.loads(response.content)

        self.assertIsNotNone(organization.payroll_configuration)
        self.assertEqual(
            organization.payroll_configuration.law_discounts.count(),
            2)

    def test_can_create_configuration_with_discount_and_additionals(self):
        # GIVEN
        type_payroll = factories.TypePayrollFactory()

        AFP = factories.LawDiscountFactory(name='AFP', porcentage=3.26)
        ARS = factories.LawDiscountFactory(name='ARS', porcentage=2.26)

        organization = OrganizationFactory(user=self.user)

        # WHEN
        response = self.query(
            """
            mutation create(
                $typePayroll: String!,
                $organization: String!,
                $discountName: String!,
                $discountPorcentage: Int!
            ){
                createPayrollConfiguration(
                    typePayroll: $typePayroll,
                    organization: $organization,
                    discounts: [{
                        name: $discountName, porcentage: $discountPorcentage
                    }],
                    additionals: [{
                        name: $discountName, porcentage: $discountPorcentage
                    }]

                ){
                    ok, errors
                }
            }
            """,
            op_name='createPayrollConfiguration',
            headers={'HTTP_AUTHORIZATION': f'JWT {self.token}'},
            variables = {
                'typePayroll': str(type_payroll.uuid),
                'organization': str(organization.uuid),
                'discountName': 'Discount Prueba',
                'discountPorcentage': 3.12
            }
        )
        # THEN
        self.assertResponseNoErrors(response)
        content_discount = json.loads(response.content)

        self.assertIsNotNone(organization.payroll_configuration)
        self.assertEqual(
            organization.payroll_configuration.law_discounts.count(), 2)
        
        self.assertEqual(
            organization.payroll_configuration.discounts.count(), 1)
        self.assertEqual(
            organization.payroll_configuration.additionals.count(), 1)