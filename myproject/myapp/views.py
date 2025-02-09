from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from .models import Recipe, Category
from .forms import RegistrationForm, RecipeForm, LoginForm, RegistrationForm


def create_recipe(request: HttpRequest):
    """Создание рецепта."""
    # На данный момент не создается, так проблема с сохранением
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            cooking_steps = form.cleaned_data['cooking_steps']
            cooking_time = form.cleaned_data['cooking_time']
            image_of_food = form.cleaned_data['image_of_food']
            ingredients = form.cleaned_data['ingredients']

            recipe = Recipe.objects.create(
                title = title,
                description = description,
                cooking_steps = cooking_steps,
                cooking_time = cooking_time,
                image_of_food = image_of_food,
                ingredients = ingredients,
            )
            recipe.save()
            return redirect('index_recipes')
        else:
            print(form.errors)
    else:
        form = RecipeForm() # Пустая форма для GET-запроса

    return render(request, 'myapp/create_recipe.html', {'form': form})


def index_recipes(request: HttpRequest):
    categories = Category.objects.filter(name__in=["Супы", "Завтраки", "Сэндвичи", "Салаты"])
    return render(request, 'myapp/index_recipes.html', {'categories': categories})


def get_five_random_recipes(request: HttpRequest):
    """Получение пяти случайных рецептов."""
    # order_by('?'): Рандомайзер порядка запроса
    random_recipes = Recipe.objects.order_by('?')[:5]
    context = {
        'random_recipes': random_recipes
    }
    return render(request, 'myapp/five_random_recipes.html', context)


def get_detailed_recipe(request: HttpRequest):
    """Получение детализированного случайного рецепта."""
    random_recipe = Recipe.objects.order_by('?').first()
    context = {
        'recipe': random_recipe
    }
    return render(request, 'myapp/detailed_recipe.html', context)


def login_view(request):  # Именно такое название функции
    if request.user.is_authenticated:
        return redirect('index_recipes')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index_recipes')
    else:
        form = LoginForm()

    return render(request, 'myapp/authorization.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index_recipes')


def register(request):
    if request.user.is_authenticated:
        return redirect('index_recipes')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():

                    # Создаем пользователя, но пока не сохраняем
                    user = form.save(commit=False)
                    user.is_active = True

                    # Сохраняем пользователя
                    user.save()
    
                    # Автоматически логиним пользователя
                    login(request, user)

                    return redirect('index_recipes')
            except Exception as e:
                # Логируем ошибку если что-то пошло не так
                print(f"Error creating user: {e}")
                form.add_error(None, "Произошла ошибка при регистрации. Попробуйте позже.")
    else:
        form = RegistrationForm()

    return render(request, 'myapp/registration.html', {'form': form})
