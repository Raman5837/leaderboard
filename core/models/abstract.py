from datetime import datetime

from django.db import models


class AbstractModel(models.Model):
    """
    Abstract Model
    """

    is_deleted: bool = models.BooleanField(default=False)
    modified_at: datetime = models.DateTimeField(auto_now=True)
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["created_at", "is_deleted"]),
        ]
