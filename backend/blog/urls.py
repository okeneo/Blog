from account.views import (
    CustomTokenObtainPairView,
    ForgotPasswordView,
    PasswordChangeView,
    RegisterView,
    ResendVerificationEmailView,
    ResetPasswordView,
    UpdateEmailView,
    UserProfileView,
    VerifyEmailUpdateView,
    VerifyEmailView,
)
from django.urls import include, path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("update-email/", UpdateEmailView.as_view(), name="update_email"),
    path("forgot-password", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend_verification_email",
    ),
    path("verify-email/", VerifyEmailView.as_view(), name="verify_email"),
    path("verify-email_update/", VerifyEmailUpdateView.as_view(), name="verify_email_update"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("user/<str:username>/", UserProfileView.as_view(), name="user_profile"),
    path("account/", include("account.urls")),
    path("post/", include("post.urls")),
]
