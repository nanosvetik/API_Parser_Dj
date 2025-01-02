from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm

@login_required
def create_post(request):
    """
    Представление для создания нового поста.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Назначаем автора
            post.save()
            form.save_m2m()  # Сохраняем ManyToMany поля (теги)
            return redirect('inspiration')  # Перенаправляем на страницу вдохновения
    else:
        form = PostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})

@login_required
def inspiration(request):
    """
    Представление для отображения списка опубликованных постов с пагинацией.
    """
    posts_list = Post.objects.published().order_by('-created_at')  # Используем кастомный менеджер
    paginator = Paginator(posts_list, 5)  # По 5 постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogapp/inspiration.html', {'page_obj': page_obj})

def post_detail(request, pk):
    """
    Представление для отображения деталей конкретного поста.
    """
    post = get_object_or_404(Post, pk=pk)  # Находим пост по его ID
    return render(request, 'blogapp/post_detail.html', {'post': post})