from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

@login_required
def create_post(request):
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

@login_required  # Только авторизованные пользователи могут просматривать посты
def inspiration(request):
    posts = Post.objects.filter(status='published')  # Получаем только опубликованные посты
    return render(request, 'blogapp/inspiration.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Находим пост по его ID
    return render(request, 'blogapp/post_detail.html', {'post': post})