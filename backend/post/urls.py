from django.urls import path

from .views import (
    PostCommentsView,
    PostDetailView,
    PostListView,
    PublishPostView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("<int:pk>/comments/", PostCommentsView.as_view(), name="post_comments"),
    path("<int:pk>/publish/", PublishPostView.as_view(), name="publish_post"),
]
