from rest_framework import status
from rest_framework.authtoken.models import Token

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.generics import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from django.contrib.auth import login, authenticate, logout
from .serializers import UserProfileSerializer


class SignUpView(APIView):
    def post(self, request, *args, **kwargs):
        """Create a new user."""
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
