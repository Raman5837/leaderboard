from typing import Union

from core.serializers.leaderboard import LeaderboardSerializer, SubmitScoreSerializer
from core.serializers.user import UserSerializer

Serializers = Union[UserSerializer, SubmitScoreSerializer, LeaderboardSerializer]
