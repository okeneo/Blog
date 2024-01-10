from account.views import CustomTokenObtainPairView, RegisterView, UserProfileView
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/<str:username>/", UserProfileView.as_view(), name="user-profile"),
    path("account/", include("account.urls")),
    path("post/", include("post.urls")),
]
