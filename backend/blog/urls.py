from account.views import RegisterView, UserProfileView
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/<str:username>/", UserProfileView.as_view(), name="user-profile"),
    path("account/", include("account.urls")),
    path("post/", include("post.urls")),
]
