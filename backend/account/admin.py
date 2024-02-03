from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    UserProfile,
    VerificationEmailToken,
    VerificationEmailUpdateToken,
    VerificationPasswordResetToken,
)


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile

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

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "bio",
                    "is_email_verified",
                ),
            },
        ),
    )


@admin.register(VerificationEmailToken)
class VerificationEmailTokenAdmin(admin.ModelAdmin):
    model = VerificationEmailToken

    list_display = (
        "user",
        "created_at",
    )


@admin.register(VerificationEmailUpdateToken)
class VerificationEmailUpdateTokenAdmin(admin.ModelAdmin):
    model = VerificationEmailUpdateToken

    list_display = (
        "user",
        "created_at",
        "new_email",
    )


@admin.register(VerificationPasswordResetToken)
class VerificationPasswordResetTokenAdmin(admin.ModelAdmin):
    model = VerificationPasswordResetToken

    list_display = (
        "user",
        "created_at",
    )
