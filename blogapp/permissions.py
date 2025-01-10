from rest_framework import permissions

class IsReader(permissions.BasePermission):
    """
    Пользователь имеет роль "Читатель".
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.role == 'reader'

class IsAuthor(permissions.BasePermission):
    """
    Пользователь имеет роль "Автор".
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.userprofile.role == 'author'

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользователь является автором поста или может только читать.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Чтение доступно всем
            return True
        return obj.author == request.user  # Редактирование доступно только автору

class IsAdmin(permissions.BasePermission):
    """
    Пользователь является администратором и имеет полные права.
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