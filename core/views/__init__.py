from typing import Union

from core.views.leaderboard import LeaderboardView, PlayerRankView, SubmitScoreView
from core.views.user import RegisterUserView

Views = Union[RegisterUserView, LeaderboardView, SubmitScoreView, PlayerRankView]
