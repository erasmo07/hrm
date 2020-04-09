import pytest
from datetime import date

from django.conf import settings
from django.test import TestCase

from celery.result import EagerResult

from hrm.contrib import enums
from hrm.payroll import tasks
from hrm.payroll.tests import factories

from hrm.users.tests.factories import OrganizationFactory, UserFactory
from hrm.collaborator.tests.factories import CollaboratorFactory


class TestPayrollTask(TestCase):

    def test_create_payrolls_success(self):
        """Success path when user init payroll."""
        # GIVEN
        type_payroll = factories.TypePayrollFactory.create()

        AFP = factories.LawDiscountFactory(name='AFP', porcentage=3.26)
        ARS = factories.LawDiscountFactory(name='ARS', porcentage=2.26)

        organization = OrganizationFactory(user=UserFactory.create())

        factories.LawDiscountOrganizationFactory.create(
            law_discount=AFP, organization=organization)
        factories.LawDiscountOrganizationFactory.create(
            law_discount=ARS, organization=organization)

        configuration = factories.PayrollConfigurationFactory.create(
            type_payroll=type_payroll, organization=organization
        )

        collaborator = CollaboratorFactory.create(organization=organization)

        settings.CELERY_TASK_ALWAYS_EAGER = True

        # WHEN
        tasks.CreatePayroll().run(configuration.id)

        # THEN
        assert (configuration.payroll_set.count() is 
                configuration.type_payroll.count_mount)
        
        assert (
            configuration.payroll_set.filter(
                status__name=enums.StatusEnums.payroll.not_initial
            ).count() is 2
        )
        
        first_payroll = configuration.payroll_set.get(
            date_apply=date(
                year=date.today().year, month=date.today().month,
                day=15))
        first_payroll_collaborator = first_payroll.payrollcollaborator_set.first()
        assert first_payroll_collaborator.law_discounts.exists() is False

        last_payroll = configuration.payroll_set.get(
            date_apply=date(
                year=date.today().year, month=date.today().month,
                day=30))
        last_payroll_collaborator = last_payroll.payrollcollaborator_set.first()
        assert last_payroll_collaborator.law_discounts.exists() is True

        assert collaborator.payroll.count() is 2
        
