from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Profile


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsReader(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == Profile.READER


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == Profile.AUTHOR

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.profile.role == Profile.ADMIN


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
