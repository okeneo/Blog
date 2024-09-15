from account.permissions import IsAdmin, IsAuthor, IsOwner, ReadOnly
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import get_object_or_404
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

    @swagger_auto_schema(
        responses={
            200: PostDetailSerializer(many=True),
        }
    )
    def get(self, request, *args, **kwargs):
        """Get all posts."""
        posts = Post.objects.all()
        serializer = PostDetailSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PostWriteSerializer,
        responses={
            201: PostWriteSerializer,
            400: "Bad Request",
            401: "Unauthorized Request",
        },
    )
    def post(self, request, *args, **kwargs):
        """Create a new post.

        The user must be authenticated and be an author.
        """
        # TODO: They must be creating a post under their account.
        serializer = PostWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ReadOnly | (IsAuthenticated & (IsAdmin | (IsAuthor & IsOwner))),)

    @swagger_auto_schema(
        response={
            200: PostDetailSerializer,
            401: "Unauthorized Request",
            404: "Post Not Found",
        }
    )
    def get(self, request, pk, *args, **kwargs):
        """Get a post."""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        response={
            200: PostWriteSerializer,
            400: "Bad Request",
            401: "Unauthorized Request",
            404: "Post Not Found",
        }
    )
    def put(self, request, pk, *args, **kwargs):
        """Update a post.

        The user must be authenticated and must be an admin or the author of the post.
        """
        post = get_object_or_404(Post, pk=pk)
        serializer = PostWriteSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        response={
            200: "Sucessful Response",
            401: "Unauthorized Request",
            404: "Post Not Found",
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        """Delete a post.

        The user must be authenticated and must be an admin or the author of the post.
        """
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_200_OK)


class PublishPostView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated & (IsAdmin | (IsAuthor & IsOwner)),)

    @swagger_auto_schema(
        responses={
            200: "Successful Response",
            400: "Bad Request",
            401: "Unauthorized Request",
            404: "Post Not Found",
        }
    )
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


class PostCommentsView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        responses={
            200: CommentTreeSerializer(many=True),
        }
    )
    def get(self, request, pk, *args, **kwargs):
        """Get all comments under a post."""
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

    @swagger_auto_schema(
        responses={
            200: "Successful Response",
            401: "Unauthorized Request",
            404: "Comment Not Found",
        }
    )
    def delete(self, request, pk, *args, **kwargs):
        """Delete a comment."""
        comment = get_object_or_404(Comment, pk=pk)

        if comment.replies.exist():
            comment.soft_delete()
        else:
            comment.delete()


class CategoryListView(APIView):
    @swagger_auto_schema(
        Categorys=["post"],
        operation_description="List all categories.",
        responses={200: CategorySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagListView(APIView):
    @swagger_auto_schema(
        tags=["post"],
        operation_description="List all tags.",
        responses={200: TagSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
