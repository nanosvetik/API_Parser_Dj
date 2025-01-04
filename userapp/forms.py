from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Поле email обязательно

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Проверка уникальности email
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']  # Поля, которые можно редактировать

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']