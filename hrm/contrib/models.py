import uuid
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    history = HistoricalRecords()

    class Meta:
        abstract = True


class Status(BaseModel):
    name = models.CharField('Status', max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name