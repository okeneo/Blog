from account.models import UserProfile
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class HasReaderRole(BasePermission):
    def has_permission(self, request, view):
        READER = UserProfile.READER
        return request.user.role == READER


class HasAuthorRole(BasePermission):
    def has_permission(self, request, view):
        AUTHOR = UserProfile.AUTHOR
        return request.user.role == AUTHOR


class HasAdminRole(BasePermission):
    def has_permission(self, request, view):
        ADMIN = UserProfile.ADMIN
        return request.user.role == ADMIN
