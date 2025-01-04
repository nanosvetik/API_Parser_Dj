from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.cache import cache
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
import logging

logger = logging.getLogger(__name__)

@login_required
def create_post(request):
    """
    Представление для создания нового поста.
    """
    if request.user.userprofile.role == 'reader':
        messages.error(request, "У вас нет прав для создания постов. Если вы хотите стать автором, отправьте запрос в вашем профиле.")
        return redirect('inspiration')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            action = request.POST.get('action')
            if action == 'moderation':
                post.status = 'moderation'
                messages.success(request, "Пост отправлен на модерацию.")
            elif action == 'publish' and request.user.userprofile.role in ['admin', 'moderator']:
                post.status = 'published'
                messages.success(request, "Пост успешно опубликован.")
            elif action == 'draft':
                post.status = 'draft'
                messages.success(request, "Пост сохранён как черновик.")
            else:
                post.status = 'moderation'
                messages.success(request, "Пост отправлен на модерацию.")

            post.save()
            form.save_m2m()  # Сохраняем ManyToMany поля (теги)
            return redirect('post_detail', pk=post.pk)
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = PostForm()

    return render(request, 'blogapp/create_post.html', {'form': form})

def inspiration(request):
    """
    Представление для отображения списка опубликованных постов с пагинацией и поиском по тегам.
    """
    # Получаем тег из GET-запроса
    tag = request.GET.get('tag')

    # Фильтруем посты по тегу, если он указан
    if tag:
        posts_list = Post.objects.filter(
            tags__name__icontains=tag
        ).select_related(
            'author__userprofile'  # Оптимизация: загружаем автора и его профиль за один запрос
        ).prefetch_related(
            'tags'  # Оптимизация: загружаем теги за один запрос
        ).order_by('-created_at')
    else:
        if request.user.is_authenticated and request.user.userprofile.role in ['admin', 'moderator']:
            # Администраторы и модераторы видят все посты
            posts_list = Post.objects.all().select_related(
                'author__userprofile'
            ).prefetch_related(
                'tags'
            ).order_by('-created_at')
        else:
            # Обычные пользователи видят только опубликованные посты
            posts_list = Post.objects.published().select_related(
                'author__userprofile'
            ).prefetch_related(
                'tags'
            ).order_by('-created_at')

    # Получаем все теги для выпадающего списка (используем кэширование)
    all_tags = cache.get('all_tags')
    if not all_tags:
        all_tags = Tag.objects.all()
        cache.set('all_tags', all_tags, timeout=60 * 15)  # Кэшируем на 15 минут

    # Получаем количество непрочитанных уведомлений
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()

    # Пагинация
    paginator = Paginator(posts_list, 5)  # По 5 постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogapp/inspiration.html', {
        'page_obj': page_obj,
        'all_tags': all_tags,  # Передаем все теги в шаблон
        'unread_notifications_count': unread_notifications_count,  # Передаем количество непрочитанных уведомлений
    })

def post_detail(request, pk):
    """
    Представление для отображения деталей поста и комментариев.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')  # Все комментарии к посту

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "Чтобы оставить комментарий, войдите в систему.")
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Ваш комментарий успешно добавлен.")
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blogapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required
def edit_post(request, pk):
    """
    Представление для редактирования поста.
    """
    post = get_object_or_404(Post, pk=pk)

    # Проверяем, что пользователь является автором, модератором или администратором
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "Вы не можете редактировать этот пост.")
        return redirect('inspiration')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)

            # Определяем действие из формы
            action = request.POST.get('action')

            if action == 'moderation':
                # Отправка на модерацию
                updated_post.status = 'moderation'
                messages.success(request, "Пост отправлен на модерацию.")
            elif action == 'draft':
                # Сохранение как черновик
                updated_post.status = 'draft'
                messages.success(request, "Пост сохранён как черновик.")
            else:
                # По умолчанию для авторов — отправка на модерацию
                updated_post.status = 'moderation'
                messages.success(request, "Пост отправлен на модерацию.")

            updated_post.save()
            form.save_m2m()  # Сохраняем ManyToMany поля (теги)
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    # Получаем аватарку из профиля пользователя
    author_avatar = post.author.userprofile.avatar.url if hasattr(post.author, 'userprofile') and post.author.userprofile.avatar else None
    return render(request, 'blogapp/edit_post.html', {'form': form, 'author_avatar': author_avatar, 'post': post})

@login_required
def delete_post(request, pk):
    """
    Представление для удаления поста.
    """
    post = get_object_or_404(Post, pk=pk)

    # Проверяем, что пользователь является автором поста, модератором или администратором
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, "Вы не можете удалить этот пост.")
        return redirect('inspiration')

    # Удаляем пост
    post.delete()
    messages.success(request, "Пост успешно удален.")
    return redirect('inspiration')