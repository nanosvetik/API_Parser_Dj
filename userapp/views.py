# userapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm, AdminProfileForm
from .models import UserProfile, Notification

# Импорты для Django REST Framework
from rest_framework import viewsets
from .serializers import UserProfileSerializer, NotificationSerializer

def register(request):
    """
    Представление для регистрации нового пользователя.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            # Автоматически авторизуем пользователя после регистрации
            login(request, user)
            return redirect('index')  # Перенаправляем на главную страницу
        else:
            # Если форма не прошла валидацию, показываем ошибки
            messages.error(request, 'Ошибка при заполнении формы. Проверьте данные.')
    else:
        form = RegisterForm()
    return render(request, 'userapp/register.html', {'form': form})

def user_login(request):
    """
    Представление для входа пользователя.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'userapp/login.html', {'form': form})

def user_logout(request):
    """
    Представление для выхода пользователя.
    """
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    """
    Представление для отображения и редактирования профиля пользователя.
    """
    user_profile = request.user.userprofile  # Получаем профиль пользователя

    # Вычисляем количество непрочитанных уведомлений
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)  # Обрабатываем форму
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('profile')  # Перенаправляем обратно на страницу профиля
    else:
        form = ProfileForm(instance=user_profile)  # Создаём форму с текущими данными

    # Передаём user_profile и unread_notifications_count в контекст шаблона
    return render(request, 'userapp/profile.html', {
        'form': form,
        'user_profile': user_profile,
        'unread_notifications_count': unread_notifications_count,
    })

# Проверка, является ли пользователь администратором
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'admin'

@user_passes_test(is_admin)
def edit_user_role(request, user_id):
    """
    Представление для редактирования роли пользователя (доступно только администраторам).
    """
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        form = AdminProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Перенаправляем на страницу списка пользователей
    else:
        form = AdminProfileForm(instance=user_profile)
    return render(request, 'userapp/edit_user_role.html', {'form': form, 'user_profile': user_profile})

@user_passes_test(is_admin)
def user_list(request):
    """
    Представление для отображения списка пользователей (доступно только администраторам).
    """
    users = UserProfile.objects.all()
    return render(request, 'userapp/user_list.html', {'users': users})

@login_required
def request_author_status(request):
    """
    Представление для обработки запроса на статус "автор".
    """
    # Получаем профиль текущего пользователя
    user_profile = request.user.userprofile

    # Проверяем, что пользователь имеет роль "читатель" и ещё не отправлял запрос
    if user_profile.role == 'reader' and not user_profile.requested_author:
        user_profile.requested_author = True  # Устанавливаем флаг запроса
        user_profile.save()  # Сохраняем изменения
        messages.success(request, 'Ваш запрос на статус "автор" успешно отправлен!')
    else:
        messages.warning(request, 'Вы уже отправили запрос или имеете другой статус.')

    # Перенаправляем пользователя на страницу профиля
    return redirect('profile')

@login_required
def notifications(request):
    """
    Представление для отображения уведомлений пользователя.
    """
    # Получаем все уведомления пользователя
    user_notifications = request.user.notifications.all().order_by('-created_at')

    # Помечаем все уведомления как прочитанные
    user_notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'userapp/notifications.html', {'notifications': user_notifications})

# ViewSet для модели UserProfile
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# ViewSet для модели Notification
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer