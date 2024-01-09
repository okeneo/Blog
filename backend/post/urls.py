from django.urls import path

from .views import (
    CategoryListView,
    DeletePostView,
    PostDetailView,
    PostListView,
    PublishPostView,
    TagListView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/publish/", PublishPostView.as_view(), name="publish-post"),
    path("<int:pk>/delete/", DeletePostView.as_view(), name="delete-post"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("tags/", TagListView.as_view(), name="tag_list"),
]
