from account.models import UserProfile
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Enter a valid email address.")

    class Meta:
        model = UserProfile
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        pass

    def clean_username(self):
        pass


class UserProfileChangeForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ("email",)
