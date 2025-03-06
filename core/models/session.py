from django.contrib.auth.models import User
from django.db import models

from core.constants import GameMode
from core.models.abstract import AbstractModel


class GameSession(AbstractModel):
    """
    Stores Game Session Data
    """

    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="games"
    )

    score = models.BigIntegerField(default=0, db_index=True)
    timestamp = models.BigIntegerField(null=False, blank=False)
    mode = models.CharField(
        max_length=64, choices=GameMode.choices, null=False, blank=False
    )
