from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserLoginSerializer, UserProfilePublicSerializer, UserSignUpSerializer


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Get token.
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        """Login a user."""
        # With TokenAuthentication, the concept of a user being logged in is not as
        # straightforward, as there is no server-side session management. Instead,
        # authentication relies on the presence and validity of the authentication
        # tokens included in each request.

        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            # Get token.
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Logout a user."""
        # TODO: Invalidate token.


class UserProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, *args, **kwargs):
        """Get the user profile."""
        # TODO: A user should be able to view any user without being authenticated but...

        # TODO: In order to get more info (e.g., their email), they would need to be authenticated
        # and need to be the user that is that made the request
        # (i.e., username == request.user or user.role == admin)
        print(request.user.__dict__)
        # TODO: What does _isauthenticated really when for TokenAuthentication?
        # print(request.user._isauthenticated)

        user = UserProfile.objects.filter(username=username)
        if not user:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserProfilePublicSerializer(user)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
