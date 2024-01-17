from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "date_joined",
        "last_login",
        "pk",
    )
    model = UserProfile
