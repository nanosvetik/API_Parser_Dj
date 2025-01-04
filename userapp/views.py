from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .forms import AdminProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import Notification

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Профиль создается автоматически через сигнал
            return redirect('index')  # Перенаправляем на главную страницу
    else:
        form = RegisterForm()
    return render(request, 'userapp/register.html', {'form': form})

def user_login(request):
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
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)  # Получаем профиль пользователя
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)  # Обрабатываем форму
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('profile')  # Перенаправляем обратно на страницу профиля
    else:
        form = ProfileForm(instance=user_profile)  # Создаём форму с текущими данными

    # Передаём user_profile в контекст шаблона
    return render(request, 'userapp/profile.html', {
        'form': form,
        'user_profile': user_profile,  # Добавляем user_profile в контекст
    })

# Проверка, является ли пользователь администратором
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'admin'

@user_passes_test(is_admin)
def edit_user_role(request, user_id):
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
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'userapp/notifications.html', {'notifications': user_notifications})