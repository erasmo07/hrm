import factory
from datetime import datetime
from factory import (
    django as fac_django,
    DjangoModelFactory,
    Faker, post_generation,
    LazyAttribute, fuzzy)

from django.core.files.base import ContentFile

from hrm.users.tests import factories as users_factories
from hrm.collaborator import models


class LevelFactory(DjangoModelFactory):
    name = Faker('name')
    organization = factory.SubFactory(
        users_factories.OrganizationFactory)

    class Meta:
        model = models.Level


class OrganizationUnitFactory(DjangoModelFactory):
    name = Faker('name')
    organization = factory.SubFactory(
        users_factories.OrganizationFactory)

    class Meta:
        model = models.OrganizationUnit


class PositionFactory(DjangoModelFactory):
    name = Faker('name')
    salary = 100.00

    organization = factory.SubFactory(
        users_factories.OrganizationFactory)
    organization_unit = factory.SubFactory(
        OrganizationUnitFactory)
    level = factory.SubFactory(
        LevelFactory
    )

    class Meta:
        model = models.Position


class StatusCollaboratorFactory(DjangoModelFactory):
    name = Faker('name')

    class Meta:
        model = models.StatusCollaborator


class CollaboratorFactory(DjangoModelFactory):
    name = Faker('name')
    last_name = Faker('last_name')
    date_admission = datetime.now().strftime("%Y-%m-%d")

    user = factory.SubFactory(
        users_factories.UserFactory)

    organization = factory.SubFactory(
        users_factories.OrganizationFactory)

    position = factory.SubFactory(
        PositionFactory
    )
    status = factory.SubFactory(
        StatusCollaboratorFactory
    )

    image = LazyAttribute(
        lambda _: ContentFile(
            fac_django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )

    class Meta:
        model = models.Collaborator
