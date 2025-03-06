from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import SubmitScoreSerializer
from core.services import LeaderboardService


class SubmitScoreView(APIView):
    """
    API View To Submit The Score
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        """ """

        serializer = SubmitScoreSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        mode = serializer.validated_data["mode"]
        score = serializer.validated_data["score"]
        user: User = serializer.validated_data["user"]

        LeaderboardService.submit_score(user.id, mode, score)
        return Response(
            {"message": "Score submitted successfully"}, status=status.HTTP_200_OK
        )


class LeaderboardView(APIView):
    """
    API View To Get Top Players
    """

    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        """ """

        _ = request
        response = [
            {"user_id": int(user_id), "score": int(score)}
            for user_id, score in LeaderboardService.get_top_players()
        ]

        return Response({"results": response}, status=status.HTTP_200_OK)


class PlayerRankView(APIView):
    """
    API View To Get Rank Of A Player
    """

    permission_classes = (AllowAny,)

    def get(self, request: Request, user_id: int) -> Response:
        """ """

        _ = request

        rank = LeaderboardService.get_player_rank(user_id)
        return Response({"rank": rank}, status=status.HTTP_200_OK)
