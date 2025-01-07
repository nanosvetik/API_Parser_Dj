from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Notification

@receiver(post_save, sender=UserProfile)
def notify_user_on_role_change(sender, instance, **kwargs):
    """
    Отправляет уведомление пользователю при изменении его роли.
    """
    if kwargs.get('created', False):  # Пропускаем создание нового профиля
        return

    try:
        old_profile = UserProfile.objects.get(pk=instance.pk)
    except UserProfile.DoesNotExist:
        return

    # Проверяем, изменилась ли роль
    if old_profile.role != instance.role:
        message = f'Ваша роль изменена на "{instance.get_role_display()}".'
        print(f"Создаём уведомление для пользователя {instance.user.username}: {message}")  # Отладочный вывод
        Notification.objects.create(user=instance.user, message=message)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создаёт профиль пользователя при регистрации.
    """
    if created:
        UserProfile.objects.create(user=instance, role='reader')