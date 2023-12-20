from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import ProfileUser


class ProfileUserCreationForm(UserCreationForm):
    class Meta:
        model = ProfileUser
        fields = ("username", "email")


class ProfileUserChangeForm(UserChangeForm):
    class Meta:
        model = ProfileUser
        fields = ("username", "email")
