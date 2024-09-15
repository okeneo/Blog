from django.contrib.auth.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsReader(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.READER


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.AUTHOR


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == User.ADMIN


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
