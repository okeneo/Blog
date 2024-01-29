from django.urls import path

from .views import (
    CategoryListView,
    PostCommentsView,
    PostDetailView,
    PostListView,
    PublishPostView,
    TagListView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/comments/", PostCommentsView.as_view(), name="post_comments"),
    path("<int:pk>/publish/", PublishPostView.as_view(), name="publish_post"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("tags/", TagListView.as_view(), name="tag_list"),
]
