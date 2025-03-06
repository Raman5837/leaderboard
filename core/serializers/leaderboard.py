from django.contrib.auth.models import User
from rest_framework import serializers

from core.constants import GameMode
from core.models.session import GameSession


class SubmitScoreSerializer(serializers.Serializer):
    """
    Serializer for submitting scores.
    """

    score = serializers.IntegerField(min_value=0)
    mode = serializers.ChoiceField(choices=GameMode.choices)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Serializer for leaderboard entries.
    """

    user_id = serializers.IntegerField(source="user.id")

    class Meta:
        model = GameSession
        fields = ["user_id", "mode", "score", "timestamp"]
