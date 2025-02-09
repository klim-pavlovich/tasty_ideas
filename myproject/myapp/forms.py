from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from myapp.models import Recipe
import re

class RecipeForm (forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'cooking_time', 'image_of_food', 'ingredients']

        widgets = {
            'title': forms.Textarea(attrs={'col': 80, 'rows': 4}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'cooking_steps': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
            'cooking_time': forms.NumberInput(attrs={'cols': 80, 'rows': 1, 'min': 1}),
            'ingredients': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
        }

    # Дополнительная валидация для поля cooking_time
    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time is not None and cooking_time < 1:
            raise forms.ValidationError('Время готовки должно быть больше 0 минут.')
        return cooking_time


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )


    error_messages = {
        'invalid_login': '',  # Убираем стандартное сообщение
        'inactive': 'Этот аккаунт неактивен.'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Введите ваш email',
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите ваш email'}
        )
    )
    
    username = forms.CharField(
        label='Придумайте пользовательское имя',
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}
        )
    )

    
    password1 = forms.CharField(
        label='Придумайте пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}
        )
    )

    
    password2 = forms.CharField(
        label='Подтвердите пароль',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
        'password_too_short': '',  # Убираем стандартное сообщение
        'password_too_similar': '',  # Убираем стандартное сообщение
        'password_entirely_numeric': ''  # Убираем стандартное сообщение
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Полностью отключаем все сообщения об ошибках для password2
        self.fields['password2'].error_messages = {
            'required': '',
            'min_length': '',
            'max_length': '',
            'password_mismatch': '',
        }
        # Отключаем обязательность поля password2 для валидации
        self.fields['password2'].required = False

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Если есть ошибки в password1, очищаем все ошибки password2
        if self.errors.get('password1'):
            if 'password2' in self.errors:
                del self.errors['password2']
            return cleaned_data

        # Проверяем совпадение паролей только если первый пароль валидный
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают')

        return cleaned_data

    def clean_password2(self):
        # Если есть ошибки в password1, пропускаем валидацию password2
        if 'password1' in self.errors:
            return self.data.get('password2', '')
        
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
            
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Проверка формата email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError('Некорректный формат email')

        # Проверка на уникальность
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Проверка длины
        if len(username) < 3:
            raise forms.ValidationError('Имя пользователя должно быть не менее 3 символов')

        # Проверка на уникальность
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято')

        return username