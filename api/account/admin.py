from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# @admin.register(User)
# class UserAdmin(UserAdmin):
#     model = User

#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": ("username", "password1", "password2", "email"),
#             },
#         ),
#     )

#     list_display = (
#         "username",
#         "email",
#         "date_joined",
#         "last_login",
#         "pk",
#     )

#     fieldsets = UserAdmin.fieldsets + (
#         (
#             "Additional Information",
#             {
#                 "fields": (
#                     "role",
#                     "bio",
#                 ),
#             },
#         ),
#     )
