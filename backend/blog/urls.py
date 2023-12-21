from django.urls import path

from .views import PostDetailView, PostListView

urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
]
