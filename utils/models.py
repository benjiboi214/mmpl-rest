import uuid as uuid_lib

from django.db import models


class TimeStampedUuidModel(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False
    )

    class Meta:
        abstract = True
        ordering = ('-created',)
