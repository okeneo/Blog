from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserProfile
from .permissions import IsAdminUser
from .serializers import (
    AccountSerializer,
    UserProfilePrivateSerializer,
    UserProfilePublicSerializer,
    UserRegisterSerializer,
)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(
                {"detail": "User registered successfully."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    def get(self, request, username, *args, **kwargs):
        """Get the user profile."""
        user = get_object_or_404(UserProfile, username=username)

        # A user must be authenticated (correspoding to the default authentication schemes,
        # which is only JWT at the time of writing) and must either be the owner of the account,
        # or have the admin role.
        if request.user.is_authenticated:
            ADMIN = UserProfile.ADMIN
            if request.user == user or request.user.role == ADMIN:
                serializer = UserProfilePrivateSerializer(user)
            else:
                serializer = UserProfilePublicSerializer(user)
        else:
            # Use the public serializer for non-authenticated users.
            serializer = UserProfilePublicSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated & IsAdminUser,)

    def get(self, request, username, *args, **kwargs):
        """Get the data of a given user."""
        user = get_object_or_404(UserProfile, username=username)

        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
