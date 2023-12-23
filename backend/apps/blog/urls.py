from django.urls import path
from rest_framework.authtoken import views

from .views import PostDetailView, PostListView

urlpatterns = [
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("api-token-auth/", views.obtain_auth_token),
]
