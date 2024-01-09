from account.models import UserProfile
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsReader(BasePermission):
    def has_permission(self, request, view):
        READER = UserProfile.READER
        return request.user.role == READER


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        AUTHOR = UserProfile.AUTHOR
        return request.user.role == AUTHOR


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        ADMIN = UserProfile.ADMIN
        return request.user.role == ADMIN


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


# class HasObjectPermission(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and (
#             request.user.is_staff or request.user.is_superuser or obj.user == request.user
#         )
