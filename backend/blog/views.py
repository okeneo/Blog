from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        """Get all posts."""
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Create a new post.

        Note: The user must be looged in and be an author.
        """
        # TODO: Check that the user is logged in.
        # TODO: Check that the user has the author role.
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        """Get a post."""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """Update a post.

        Note: The user must be logged in and must be an admin or the author of the post.
        """
        # TODO: Check that the user is logged in.
        # TODO: Check that the user is an admin or the author of the post.
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """Delete a post.

        Note: The user must be logged in and must be an admin or the author of the post.
        """
        # TODO: Check that the user is logged in.
        # TODO: Check that the user is an admin or the author of the post.
        if request.user.is_authenticated:
            # TODO: Check that the user is an admin or the author of the post.
            post = get_object_or_404(Post, pk=pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)
