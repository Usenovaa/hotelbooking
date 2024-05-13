from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view, obj=None):
        return request.user.is_authenticated and request.user.is_superuser


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user

