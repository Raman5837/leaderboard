from typing import Union

from core.models.abstract import AbstractModel
from core.models.session import GameSession

Models = Union[GameSession, AbstractModel]
