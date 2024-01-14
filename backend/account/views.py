from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile
from .permissions import IsAdminUser, IsOwner, ReadOnly
from .serializers import (
    AccountSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ReadOnly | (IsAuthenticated & IsOwner),)

    def get(self, request, username, *args, **kwargs):
        """Get the user profile.

        The user must be logged in (authenticated) and must either be the owner of the account,
        or have the admin role in order to view private data.
        """
        user = get_object_or_404(UserProfile, username=username)

        if request.user.is_authenticated:
            ADMIN = UserProfile.ADMIN
            if request.user == user or request.user.role == ADMIN:
                serializer = UserProfilePrivateSerializer(user)
            else:
                # Use the public serializer for users that do not have the admin role.
                serializer = UserProfilePublicSerializer(user)
        else:
            # Use the public serializer for non-authenticated users.
            serializer = UserProfilePublicSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username, *args, **kwargs):
        """Update the information of a user."""
        user = get_object_or_404(UserProfile, username=username)
        serializer = UserProfilePrivateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated & IsAdminUser,)

    def get(self, request, username, *args, **kwargs):
        """Get the data of a given user."""
        user = get_object_or_404(UserProfile, username=username)

        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordChangeView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated & IsOwner,)

    def put(self, request, username, *args, **kwargs):
        user = get_object_or_404(UserProfile, username=username)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password1"])
            user.save()
            return Response(
                {"detail", "Password changed successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
