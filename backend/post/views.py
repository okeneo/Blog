from account.permissions import IsAdminUser, IsAuthor, IsOwner, ReadOnly
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Category, Comment, Post, Tag
from .serializers import (
    CategorySerializer,
    CommentTreeSerializer,
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
        # They must be creating a post under their account.
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


class PostCommentsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        top_level_comments = Comment.objects.filter(post=post, parent_comment__isnull=True)
        serializer = CommentTreeSerializer(top_level_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        # They must be creating a comment under their account.
        pass


class CommentDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ReadOnly | (IsAuthenticated & IsOwner),)

    def get(self, request, pk, *args, **kwargs):
        pass

    def put(self, request, pk, *args, **kwargs):
        pass

    def delete(self, request, pk, *args, **kwargs):
        """Delete a comment."""
        comment = get_object_or_404(Comment, pk=pk)

        if comment.filter(parent_comment__isnull=False):
            comment.delete()
        else:
            comment.soft_delete()
