from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Пользователь является администратором.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.role == 'admin'

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Админ имеет полные права, остальные — только чтение.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Чтение доступно всем
            return True
        return request.user.is_authenticated and request.user.userprofile.role == 'admin'