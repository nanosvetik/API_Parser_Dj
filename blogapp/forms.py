from django import forms
from .models import Post, Tag

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),  # Все доступные теги
        widget=forms.CheckboxSelectMultiple,  # Чекбоксы для выбора
        required=False  # Необязательное поле
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags']