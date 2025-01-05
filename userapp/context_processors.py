from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile
from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_notifications_count}
    return {}

def user_role(request):
    """
    Контекстный процессор для добавления роли пользователя в контекст шаблонов.
    """
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            return {'user_role': profile.role}
        except ObjectDoesNotExist:
            return {'user_role': None}  # Или установите значение по умолчанию
    return {}