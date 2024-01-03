from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile
from .serializers import UserLoginSerializer, UserProfileSerializer, UserSignUpSerializer


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
        # Note that with TokenAuthentication, the concept of a user being logged in
        # is not as straightforward, as there is no server-side session management.
        # Instead, authentication relies on the presence and validity of authentication
        # tokens included in each request.

        # Check if the user is already logged in.
        # TODO: Does the request have a tokem in it already? If yes, send a bad request.

        # TODO: Compare this view with ObtainAuthToken.
        # Are we checking _isauthenticated at all? Is this even required? What does this
        # really check in the context of TokenAuthentication.

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
        # Note that with TokenAuthentication, the concept of a user being logged in
        # is not as straightforward, as there is no server-side session management.
        # Instead, authentication relies on the presence and validity of authentication
        # tokens included in each request.

        # TODO: A user should be able to view any user without being authenticated.

        # TODO: In order to get more info (e.g., their email), they would need to be authenticated and
        # need to be the user that is that made the request
        # (i.e., username == request.user or user.role == admin)
        print(request.user.__dict__)
        # TODO: What does _isauthenticated really when for TokenAuthentication?
        # print(request.user._isauthenticated)

        user = UserProfile.objects.filter(username=username)
        if not user:
            return Response(
                {"error": f"The user with username '{username}' was not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserProfileSerializer(data=user)
        # TODO: 
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
