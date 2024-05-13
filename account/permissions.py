from rest_framework.permissions import BasePermission


class IsActivePermission(BasePermission):
    def has_permission(self, request, view, obj=None):
        return bool(request.user and request.user.is_active)
