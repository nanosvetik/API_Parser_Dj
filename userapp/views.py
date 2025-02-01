from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, AdminProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Notification

from rest_framework import generics, permissions
from .serializers import UserProfileSerializer, NotificationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

def register(request):
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
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Генерация токена
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Сохранение токенов в сессии
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token

                return redirect('profile')  # Перенаправляем на страницу профиля
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = LoginForm()
    return render(request, 'userapp/login.html', {'form': form})

def user_logout(request):
    # Очищаем сессию
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'refresh_token' in request.session:
        del request.session['refresh_token']

    # Выход пользователя
    logout(request)
    return redirect('index')  # Перенаправляем на главную страницу

@login_required
def profile(request):
    user_profile = request.user.userprofile  # Получаем профиль пользователя

    # Вычисляем количество непрочитанных уведомлений
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    # Получаем токен из сессии (если он есть)
    user_token = request.session.get('access_token')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)  # Обрабатываем форму
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect('profile')  # Перенаправляем обратно на страницу профиля
    else:
        form = ProfileForm(instance=user_profile)  # Создаём форму с текущими данными

    # Передаём user_profile, unread_notifications_count и user_token в контекст шаблона
    return render(request, 'userapp/profile.html', {
        'form': form,
        'user_profile': user_profile,
        'unread_notifications_count': unread_notifications_count,
        'user_token': user_token,  # Передаём токен в шаблон
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
    # Получаем все уведомления пользователя
    user_notifications = request.user.notifications.all().order_by('-created_at')

    # Помечаем все уведомления как прочитанные
    user_notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'userapp/notifications.html', {'notifications': user_notifications})

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile

class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-created_at')

class TokenObtainPairViewWithUserData(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.user
            response.data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            # Убедитесь, что refresh_token возвращается
            response.data['refresh'] = str(response.data['refresh'])
        return response

class TokenRefreshViewWithUserData(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.request.user
            response.data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        return response

class TokenRefreshAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=400)