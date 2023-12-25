from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "pk",
    )
    model = UserProfile
