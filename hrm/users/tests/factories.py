from typing import Any, Sequence

from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from factory import (
    DjangoModelFactory, Faker,
    post_generation, SubFactory,
    LazyAttribute)

from hrm.users import models



class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        self.set_password('@1234567')
        self.organization = SubFactory(OrganizationFactory)
        self.save()

        self.user_permissions.set(Permission.objects.all())

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class OrganizationFactory(DjangoModelFactory):
    name = Faker('name')
    principal_email = LazyAttribute(
        lambda o: '%s@example.org' % o.name.lower())

    user = SubFactory(UserFactory)

    class Meta:
        model = models.Organization

