from django.urls import path

from .views import AccountView

urlpatterns = [
    path("<str:username>/", AccountView.as_view(), name="account"),
]
