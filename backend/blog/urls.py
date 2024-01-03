from account.views import LoginView, LogoutView, SignUpView, UserProfileView
from django.urls import include, path

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("<str:username>/", UserProfileView.as_view(), name="user-profile"),
    path("post/", include("post.urls")),
]
