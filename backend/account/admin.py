from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserProfileChangeForm, UserProfileCreationForm
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    add_form = UserProfileCreationForm
    form = UserProfileChangeForm
    model = UserProfile
