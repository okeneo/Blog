from account.views import (
    CustomTokenObtainPairView,
    EmailConfirmationView,
    RegisterView,
    ResendVerificationEmailView,
    UserProfileView,
)
from django.urls import include, path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", EmailConfirmationView.as_view(), name="email_confimation"),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend-verification-email",
    ),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("user/<str:username>/", UserProfileView.as_view(), name="user-profile"),
    path("account/", include("account.urls")),
    path("post/", include("post.urls")),
]
