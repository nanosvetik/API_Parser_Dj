from django import forms
from .models import Post, Tag
from django.contrib.auth import get_user_model
from .models import Comment


User = get_user_model()


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Убрали поле status

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обновляем атрибуты для оставшихся полей
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': 5})
        self.fields['tags'].widget.attrs.update({'class': 'form-check-input'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Поле для текста комментария
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
