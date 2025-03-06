from datetime import datetime
from json import dumps
from typing import Any, List, Optional, Tuple

from django.db import transaction

from core.config import RedisClient, RedisKey
from core.models import GameSession


class LeaderboardService:
    """ """

    __redis = RedisClient()
    SCORE_QUEUE = RedisKey.SCORE_QUEUE.value
    LEADERBOARD_KEY = RedisKey.LEADERBOARD.value

    @staticmethod
    def submit_score(user_id: int, mode: str, score: int) -> None:
        """
        Increments user score in Redis and triggers async DB update.
        """

        LeaderboardService.__redis.zincrby(
            LeaderboardService.LEADERBOARD_KEY, score, user_id
        )

        # Push event to Redis queue for async processing
        event = dumps({"user_id": user_id, "mode": mode, "score": score})
        LeaderboardService.__redis.push(LeaderboardService.SCORE_QUEUE, event)

    @staticmethod
    def persist_session(user_id: int, mode: str, score: int) -> None:
        """
        Saves the game session data in the database.
        """

        with transaction.atomic():
            GameSession.objects.create(
                mode=mode,
                score=score,
                user_id=user_id,
                timestamp=int(datetime.now().timestamp()),
            )

    @staticmethod
    def get_top_players(limit: int = 10) -> List[Tuple[str, Any]]:
        """
        Retrieves top N players from Redis.
        """

        return LeaderboardService.__redis.zrevrange(
            LeaderboardService.LEADERBOARD_KEY, 0, limit - 1, withscores=True
        )

    @staticmethod
    def get_player_rank(user_id: int) -> Optional[int]:
        """
        Fetches player's current rank.
        """

        rank = LeaderboardService.__redis.zrevrank(
            LeaderboardService.LEADERBOARD_KEY, user_id
        )
        # +1 because zrevrank returns zero-based ranking.
        return rank + 1 if rank is not None else None
