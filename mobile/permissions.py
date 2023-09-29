from rest_framework.permissions import BasePermission


class UserPermisions(BasePermission):
    def has_permission(self, request, view):
        return True
