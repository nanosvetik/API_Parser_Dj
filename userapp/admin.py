from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Отображаемые поля
    list_filter = ('role',)  # Фильтры
    search_fields = ('user__username',)  # Поиск по имени пользователя
    fieldsets = (
        (None, {
            'fields': ('user', 'role')  # Основные поля
        }),
        ('Дополнительно', {
            'fields': (),  # Дополнительные поля (если есть)
            'classes': ('collapse',)  # Сворачиваемый блок
        }),
    )
    readonly_fields = ('user',)  # Поле "user" только для чтения