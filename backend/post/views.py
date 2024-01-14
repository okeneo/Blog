from account.permissions import IsAdminUser, IsAuthor, IsOwner, ReadOnly
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Post, Tag
from .serializers import (
    CategorySerializer,
    PostDetailSerializer,
    PostWriteSerializer,
    TagSerializer,
)


class PostListView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ReadOnly | (IsAuthenticated & IsAuthor),)

    def get(self, request, *args, **kwargs):
        """Get all posts."""
        posts = Post.objects.all()
        serializer = PostDetailSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Create a new post.

        The user must be logged in (authenticated) and be an author.
        """
        serializer = PostWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ReadOnly | (IsAuthenticated & (IsAdminUser | (IsAuthor & IsOwner))),)

    def get(self, request, pk, *args, **kwargs):
        """Get a post."""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        """Update a post.

        The user must be logged in (authenticated) and must be an admin or the author of the post.
        """
        post = get_object_or_404(Post, pk=pk)
        serializer = PostWriteSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """Delete a post.

        The user must be logged in (authenticated) and must be an admin or the author of the post.
        """
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class PublishPostView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated & (IsAdminUser | (IsAuthor & IsOwner)),)

    def post(self, request, pk, *args, **kwargs):
        """Publish an existing post."""
        post = get_object_or_404(Post, pk=pk)
        if not post.published:
            post.published = True
            post.publish_date = timezone.now()
            post.save()

            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "The post is already published."}, status=status.HTTP_400_BAD_REQUEST
            )


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
