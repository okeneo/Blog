from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError
from django.db import transaction
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile, VerificationToken
from .permissions import IsAdminUser, IsOwner, ReadOnly
from .serializers import (
    AccountSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    UserProfilePrivateSerializer,
    UserProfilePublicSerializer,
    UserRegisterSerializer,
    VerificationTokenSerializer,
)
from .utils import perform_resend_verification, send_verification_email


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = UserRegisterSerializer(data=request.data)
        with transaction.atomic():
            try:
                if serializer.is_valid():
                    user = serializer.save()

                    # Send verification email.
                    token = VerificationToken.objects.create(user=user)
                    send_verification_email("registration", user.email, token.key, token)

                    return Response(
                        {"detail": "User created successfully. Email verification email sent."},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except BadHeaderError:
                # We need to manually rollback database changes if the exception is caught.
                transaction.set_rollback(True)
                return Response(
                    {"error": "Bad email header in the provided email."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class EmailConfirmationView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "token_key": self.request.query_params.get("token_key"),
        }
        serializer = VerificationTokenSerializer(data=data)
        if serializer.is_valid():
            # Set is_active and is_email_verified to True to indicate successful user registration.
            token_key = serializer.validated_data["token_key"]
            token = VerificationToken.objects.get(key=token_key)
            user = token.user
            user.is_active = True
            user.is_email_verified = True
            user.save()

            # Delete the token once the user has been registered successfully.
            token.delete()

            return Response(
                {"detail": "User registered successfully."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token, user = perform_resend_verification(email)
        except ValidationError as e:
            # Fix timing issue on resends - Tokens not expiring. Examine is_expired **property**

            # Trigger the UUID clashing issue.

            # Can you include status code info when yiu manually raise validatioEror?

            # Implement logging

            # Continue Passwords.
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            try:
                # Reaching this point, means the token has not exceeded the maximum number of send
                # attempts, so we create a new token for another send attempt.
                curr_send_attempts = token.send_attempts
                token.delete()
                token = VerificationToken.objects.create(user=user)
                token.send_attempts = curr_send_attempts
                token.save(update_fields=["send_attempts"])

                # Send verification email.
                send_verification_email("registration", token.user.email, token.key, token)

                return Response(
                    {"detail": "Email verification email resent."},
                    status=status.HTTP_204_NO_CONTENT,
                )

            except BadHeaderError:
                transaction.set_rollback(True)
                return Response(
                    {"error": "Bad email header in the provided email."},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class CustomTokenObtainPairView(TokenObtainPairView):
    """A custom view for user authentication using JWT."""

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
    permission_classes = (IsAuthenticated & (IsOwner | IsAdminUser),)

    def get(self, request, username, *args, **kwargs):
        """Get the data of a given user."""
        user = get_object_or_404(UserProfile, username=username)

        # Only users with the admin role should be able to view the data provided
        # in the AccountSerializer.
        if user.role != UserProfile.ADMIN:
            return Response(
                {"detail": "You do not have the permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = AccountSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, username, *args, **kwargs):
        """Delete a user.

        Django officially recommends setting is_active to False on delete."""
        user = get_object_or_404(UserProfile, username=username)
        user.is_active = False
        user.save()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


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


class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            "token": self.request.query_params.get("token"),
        }
        serializer = VerificationTokenSerializer(data=data)
        if serializer.is_valid():
            print()


class ForgotPasswordView(APIView):
    def post(self, request, email, *args, **kwargs):
        user = get_object_or_404(UserProfile, email=email)
        # If the user reaches this view, we should set them as inactive until they create
        # a choose a new password.
        user.is_active = False

        # If the user was not the one that clicked forgot password, then they should click a link,
        # that will go to my email box so that I can inspect the issue.
