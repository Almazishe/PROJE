import uuid
from django.db import models

class BaseModel(models.Model):
    ''' BASE MODEL '''
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='UUID',
    )

    class Meta:
        abstract = True
        ordering = ('-uuid', )

    def __str__(self) -> str:
        return str(self.uuid)


class DateModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creation date',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updation date',
    )

    class Meta:
        abstract = True
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.created_at)
