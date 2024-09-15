from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Profile
from .permissions import IsAdmin, IsUser, ReadOnly
from .serializers import ProfileSerializer, UserRegisterSerializer, UserSerializer


class UserRegisterView(APIView):
    @swagger_auto_schema(
        tags=["user"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password1": openapi.Schema(type=openapi.TYPE_STRING),
                "password2": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=[
                "username",
                "password1",
                "password2",
            ],
        ),
        responses={
            201: "Created",
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User created successfully."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ReadOnly | (IsAuthenticated & (IsUser | IsAdmin)),)

    @swagger_auto_schema(
        tags=["user"],
        manual_parameters=[
            openapi.Parameter(
                "username", openapi.IN_PATH, description="Username", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: ProfileSerializer,
            400: "Bad Request",
            404: "User Not Found",
        },
    )
    def get(self, request, username, *args, **kwargs):
        """Get a user's information."""
        user = get_object_or_404(User, username=username)
        profile = user.profile

        if request.user.is_authenticated:
            if request.user == user or request.user.profile.role == Profile.ADMIN:
                serializer = UserSerializer(user)
            else:
                # Use the public serializer for users that do not have the admin role.
                serializer = ProfileSerializer(profile)
        else:
            # Use the public serializer for non-authenticated users.
            serializer = ProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["user"],
        request_body=UserSerializer,
        manual_parameters=[
            openapi.Parameter(
                "username", openapi.IN_PATH, description="Username", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: UserSerializer,
            400: "Bad Request",
            401: "Unauthorized Request",
            404: "User Not Found",
        },
    )
    def put(self, request, username, *args, **kwargs):
        """Update a user's information."""
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["user"],
        manual_parameters=[
            openapi.Parameter(
                "username", openapi.IN_PATH, description="Username", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: "Successful Response",
            400: "Bad Request",
            401: "Unauthorized Request",
            404: "User Not Found",
        },
    )
    def delete(self, request, username, *args, **kwargs):
        """Delete a user."""
        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)

        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_200_OK)
