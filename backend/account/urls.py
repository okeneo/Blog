from account.views import LoginView, SignUpView
from django.urls import path

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    # path("logout/"),
    # path("user/")
]
