from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hrm.contrib.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField('Email', max_length=254, unique=True)


class Organization(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    principal_email = models.EmailField(
        _("Principal Email"), max_length=254, unique=True)

    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)