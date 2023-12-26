from django.urls import path
from account.views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    # path("login/"),
    # path("logout/"),
    # path("user/")
]
