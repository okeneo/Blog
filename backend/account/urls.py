from django.urls import path

from .views import UserRegisterView, UserView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("<str:username>/", UserView.as_view(), name="user"),
]
