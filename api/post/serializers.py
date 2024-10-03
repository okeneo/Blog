from account.serializers import ProfileSerializer
from rest_framework import serializers

from .models import Category, Comment, Post, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CommentTreeSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_replies(self, obj):
        # Recursively serialize replies. `replies` represents the immediate children
        # of a particular comment.
        replies = Comment.objects.filter(post=obj.post, parent_comment=obj)
        serializer = CommentTreeSerializer(replies, many=True)
        return serializer.data


class PostDetailSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = [
            "date_created",
            "date_modified",
            "publish_date",
            "published",
        ]
