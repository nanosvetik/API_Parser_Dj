from django.contrib import admin
from .models import Post, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в списке постов
    list_display = ('title', 'author', 'status', 'created_at', 'is_on_moderation')
    # Поля, по которым можно фильтровать
    list_filter = ('status', 'created_at', 'author')
    # Поля, по которым можно искать
    search_fields = ('title', 'content', 'author__username')
    # Поля, которые можно редактировать прямо из списка
    list_editable = ('status',)
    # Разделение на страницы (по 20 постов на странице)
    list_per_page = 20

    # Метод для отображения, находится ли пост на модерации
    def is_on_moderation(self, obj):
        return obj.status == 'moderation'
    is_on_moderation.short_description = 'На модерации'
    is_on_moderation.boolean = True  # Отображать как значок (галочка/крестик)

# Регистрируем модель Tag без изменений
admin.site.register(Tag)
# Register your models here.
