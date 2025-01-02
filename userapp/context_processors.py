from .models import UserProfile

def user_role(request):
    """
    Контекстный процессор для добавления роли пользователя в контекст шаблонов.
    """
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        return {'user_role': profile.role}
    return {}