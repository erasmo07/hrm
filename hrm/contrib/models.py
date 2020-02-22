import uuid
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    uuid = models.CharField(max_length=120, default=uuid.uuid4, editable=False)
    history = HistoricalRecords()

    class Meta:
        abstract = True