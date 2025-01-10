# parserapp/permissions.py
from rest_framework import permissions

class CanSearchVacancies(permissions.BasePermission):
    """
    Разрешает незарегистрированным пользователям выполнять POST-запросы для поиска вакансий.
    """
    def has_permission(self, request, view):
        if view.action == 'search':  # Разрешаем POST-запросы только для действия 'search'
            return True
        return request.user and request.user.is_authenticated  # Для остальных действий требуется авторизация