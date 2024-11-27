from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import Recipe

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RecipeForm (forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_time', 'coocking_time', 'image_of_food', 'ingredients']

        widgets = {
            'title': forms.Textarea(attrs={'col': 80, 'rows': 4}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 4}),
            'cooking_time': forms.Textarea(attrs={'cols': 80, 'rows': 6}),
            'coocking_time': forms.NumberInput(attrs={'cols': 80, 'rows': 1, 'min': 1}),
            'image_of_food': forms.ClearableFileInput(attrs={'multiple': False}),
        }
    
     # Дополнительная валидация для поля cooking_time
    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time is not None and cooking_time < 1:
            raise forms.ValidationError('Время готовки должно быть больше 0 минут.')
        return cooking_time