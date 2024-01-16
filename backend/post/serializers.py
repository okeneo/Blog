from account.serializers import UserProfilePublicSerializer
from rest_framework import serializers

from .models import Category, Post, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving detailed information about a post. Includes nested
    serializers for tags, category, and author.
    """

    author = UserProfilePublicSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts."""

    class Meta:
        model = Post
        exclude = [
            "date_created",
            "date_modified",
            "publish_date",
            "published",
        ]
