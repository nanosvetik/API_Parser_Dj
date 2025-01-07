from django.contrib import admin
from .models import UserProfile, Notification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'requested_author', 'avatar_preview', 'has_pending_request')  # Отображаемые поля
    list_filter = ('role', 'requested_author')  # Фильтры
    search_fields = ('user__username',)  # Поиск по имени пользователя
    actions = ['approve_author_requests']  # Действие для одобрения запросов

    # Метод для отображения аватарки
    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />'
        return "Аватарка отсутствует"
    avatar_preview.short_description = 'Аватарка'
    avatar_preview.allow_tags = True

    # Метод для отображения статуса запроса
    def has_pending_request(self, obj):
        return obj.requested_author
    has_pending_request.boolean = True  # Отображать как значок (галочка/крестик)
    has_pending_request.short_description = 'Запрос на статус "автор"'

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
    approve_author_requests.short_description = 'Одобрить запросы на статус "автор"'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')  # Отображаемые поля
    list_filter = ('is_read', 'created_at')  # Фильтры
    search_fields = ('user__username', 'message')  # Поиск по имени пользователя и сообщению