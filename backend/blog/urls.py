from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("post/", include("post.urls")),
    path("api-token-auth/", views.obtain_auth_token),
]
