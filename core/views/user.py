from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import UserSerializer


class RegisterUserView(APIView):
    """
    API View to Register a New User
    """

    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        """
        Registers a new user.
        """

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data={"message": "User created successfully", "user_id": user.id},
        )
