from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("user/", include("account.urls")),
    path("api-token-auth/", views.obtain_auth_token),
    path("post/", include("post.urls")),
]
