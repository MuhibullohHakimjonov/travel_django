from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Article, Comments, Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'from-control',
        'placeholder': 'Пар0ль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'forms-control',
        'placeholder': 'Подтвердите пароль'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Электронная почта'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'image', 'description', 'category', 'author']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            "author": forms.Select(attrs={
                "class": "form-control"
            })
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Комментарии', widget=forms.TextInput(attrs={
        "class": 'form-control',
        'rows': 3
    }))

    class Meta:
        model = Comments
        fields = ['content']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Фамилия пользователя'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Электронная почта'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
