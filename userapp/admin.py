from django.contrib import admin
from .models import UserProfile
from .models import Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'requested_author', 'avatar_preview')  # Отображаемые поля
    list_filter = ('role', 'requested_author')  # Фильтры
    search_fields = ('user__username',)  # Поиск по имени пользователя
    actions = ['approve_author_requests']  # Добавляем действие для одобрения запросов

    # Метод для отображения аватарки
    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />'
        return "Аватарка отсутствует"
    avatar_preview.short_description = 'Аватарка'
    avatar_preview.allow_tags = True

    # Действие для одобрения запросов на статус "автор"
    def approve_author_requests(self, request, queryset):
        for profile in queryset:
            if profile.requested_author and profile.role == 'reader':
                profile.role = 'author'
                profile.requested_author = False
                profile.save()
                # Создаём уведомление для пользователя
                Notification.objects.create(
                    user=profile.user,
                    message='Ваш запрос на статус "автор" одобрен.'
                )
        self.message_user(request, 'Запросы на статус "автор" успешно одобрены.')