from django.db.models import TextChoices


class GameMode(TextChoices):
    """
    Available Game Modes
    """

    SINGLE = "SINGLE"
    MULTI_PLAYER = "MULTI_PLAYER"
