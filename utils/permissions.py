from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_superuser or request.user.is_staff:
                return True
            else:
                return False


class IsAuthenticatedAndProfileOwnerOrReadOnly(
        permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_superuser or request.user.is_staff:
                return True
            else:
                return obj.user == request.user
