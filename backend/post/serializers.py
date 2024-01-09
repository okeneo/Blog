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
    tags = TagSerializer(many=True)
    category = CategorySerializer()
    author = UserProfilePublicSerializer()

    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = [
            "date_created",
            "date_modified",
            "publish_date",
            "published",
        ]
