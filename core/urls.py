from django.urls import path

from core.views import (
    LeaderboardView,
    PlayerRankView,
    RegisterUserView,
    SubmitScoreView,
)

urlpatterns = [
    path("leaderboard/submit", SubmitScoreView.as_view(), name="submit-score"),
    path("leaderboard/top", LeaderboardView.as_view(), name="get-leaderboard"),
    path("user/register", RegisterUserView.as_view(), name="register-user"),
    path(
        "leaderboard/rank/<int:user_id>",
        PlayerRankView.as_view(),
        name="get-player-rank",
    ),
]
