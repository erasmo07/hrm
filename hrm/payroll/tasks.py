from datetime import date

from celery import Task
from django.contrib.auth import get_user_model

from config import celery_app
from hrm.contrib import enums

from . import models

User = get_user_model()


@celery_app.task()
def create_payroll_collaborators(payroll_id, model_payroll=models.Payroll):
    payroll = model_payroll.objects.get(id=payroll_id)

    for collaborator in payroll.configuration.organization.collaborator_set.all():
        instance = models.PayrollCollaborator.objects.create(
            payroll_id=payroll_id, collaborator=collaborator
        )

        if (
            payroll.period.order is 
            payroll.configuration.type_payroll.count_mount
        ):
            instance.law_discounts.add(
                *payroll.configuration.organization.law_discounts.all())
    return True


class CreatePayroll(Task):
    _model_period = models.Period
    _model_configuration = models.PayrollConfiguration
    _model_payroll = models.Payroll
    _status_enums = enums.StatusEnums.payroll
    _create_payroll_collaborator = create_payroll_collaborators
    _configuration = None
    name = 'hrm.payroll.tasks.CreatePayroll'

    configuration_id = None

    @property
    def configuration(self):
        if not self._configuration and self.configuration_id:
            self._configuration = self._model_configuration.objects.get(
                id=self.configuration_id)
        return self._configuration
    
    @property
    def status_payroll(self):
        status_payroll, _ = models.StatusPayroll.objects.get_or_create(
            name=enums.StatusEnums.payroll.not_initial
        )
        return status_payroll

    def run(self, configuration_id, *args, **kwargs):
        self.configuration_id = configuration_id

        current_date = date.today()
        for order in range(self.configuration.type_payroll.count_mount):
            period = models.Period.objects.create(
                day_apply=15 * (order + 1), order=order + 1
            )

            date_apply = date(
                day=period.day_apply,
                month=current_date.month,
                year=current_date.year,
            )

            payroll = models.Payroll.objects.create(
                configuration_id=configuration_id,
                date_apply=date_apply,
                period=period,
                status=self.status_payroll,
            )

            self._create_payroll_collaborator.delay(payroll.id)
        return True


celery_app.tasks.register(CreatePayroll())