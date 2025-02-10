from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Recipe, Category, RecipeCategory, UnitChoices
from .forms import RegistrationForm, RecipeForm, LoginForm, RegistrationForm
from django.core.exceptions import ValidationError


@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    recipe = form.save(commit=False)
                    recipe.author = request.user
                    
                    # Подготовка и валидация ингредиентов
                    ingredients = []
                    ingredient_names = request.POST.getlist('ingredient_name[]')
                    ingredient_amounts = request.POST.getlist('ingredient_amount[]')
                    ingredient_units = request.POST.getlist('ingredient_unit[]')
                    
                    # Проверяем все строки ингредиентов
                    if len(ingredient_names) != len(ingredient_amounts) or len(ingredient_names) != len(ingredient_units):
                        form.add_error(None, 'Ошибка в данных ингредиентов')
                        raise ValidationError('Ошибка в данных ингредиентов')

                    # Проверяем каждую строку ингредиентов, включая пустые
                    for i in range(len(ingredient_names)):
                        name = ingredient_names[i].strip()
                        amount = ingredient_amounts[i].strip()
                        unit = ingredient_units[i]
                        
                        # Проверяем каждую строку, даже если она пустая
                        if not name and not amount:
                            # Пропускаем полностью пустую строку, только если это не единственная строка
                            if len(ingredient_names) == 1:
                                form.add_error(None, 'Добавьте хотя бы один ингредиент')
                                raise ValidationError('Добавьте хотя бы один ингредиент')
                            continue
                            
                        # Если хотя бы одно поле заполнено, оба должны быть заполнены
                        if not name or not amount:
                            form.add_error(None, 'Все поля ингредиентов должны быть заполнены')
                            raise ValidationError('Все поля ингредиентов должны быть заполнены')
                            
                        # Проверка на числовое значение
                        if not amount.replace(',', '').replace('.', '').isdigit():
                            form.add_error(None, 'Количество ингредиента должно быть числом')
                            raise ValidationError('Количество ингредиента должно быть числом')
                            
                        ingredients.append({
                            'name': name,
                            'amount': amount,
                            'unit': unit
                        })
                    
                    # Проверяем, что есть хотя бы один валидный ингредиент
                    if not ingredients:
                        form.add_error(None, 'Добавьте хотя бы один ингредиент')
                        raise ValidationError('Добавьте хотя бы один ингредиент')
                    
                    recipe.ingredients = ingredients
                    
                    # Проверка и сохранение шагов приготовления
                    cooking_steps = [step.strip() for step in request.POST.getlist('cooking_step[]') if step.strip()]
                    if not cooking_steps:
                        form.add_error(None, 'Добавьте хотя бы один шаг приготовления')
                        raise ValidationError('Добавьте хотя бы один шаг приготовления')
                    recipe.cooking_steps = cooking_steps
                    
                    # Проверка категорий
                    if not request.POST.getlist('categories'):
                        form.add_error(None, 'Выберите хотя бы одну категорию')
                        raise ValidationError('Выберите хотя бы одну категорию')
                    
                    recipe.save()
                    
                    # Сохранение категорий
                    for category_id in request.POST.getlist('categories'):
                        RecipeCategory.objects.create(
                            recipe=recipe,
                            category_id=category_id
                        )
                    
                    messages.success(request, 'Рецепт успешно создан!')
                    return redirect('recipe_detail', recipe_id=recipe.id)
                    
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, 'Произошла ошибка при сохранении рецепта')
                print(f"Error saving recipe: {e}")
    else:
        form = RecipeForm()

    return render(request, 'myapp/create_recipe.html', {
        'form': form,
        'categories': Category.objects.all(),
        'units': UnitChoices.choices,
    })

def recipes_page(request: HttpRequest):
    return render(request, 'myapp/recipes_page.html')


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


def login_view(request):
    """Авторизация пользователя."""
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
    """Выход из профиля."""
    logout(request)
    return redirect('index_recipes')



def register(request):
    """Регистрация пользователя."""
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

@login_required(login_url='login')
def my_recipes(request):
    """Мои рецепты."""
    user_recipes = Recipe.objects.filter(author=request.user).order_by('-date_of_create')
    return render(request, 'myapp/my_recipes.html', {'recipes': user_recipes})


def categories(request: HttpRequest):
    """Категории рецептов."""
    all_categories = Category.objects.all()
    return render(request, 'myapp/categories.html', {'categories': all_categories})


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            try:
                with transaction.atomic():
                    recipe = form.save(commit=False)
                    
                    # Подготовка ингредиентов
                    ingredients = []
                    ingredient_names = request.POST.getlist('ingredient_name[]')
                    ingredient_amounts = request.POST.getlist('ingredient_amount[]')
                    ingredient_units = request.POST.getlist('ingredient_unit[]')
                    
                    # Проверяем, что все списки имеют одинаковую длину
                    min_length = min(len(ingredient_names), len(ingredient_amounts), len(ingredient_units))
                    
                    for i in range(min_length):
                        if ingredient_names[i].strip():  # Проверяем, что название не пустое
                            ingredients.append({
                                'name': ingredient_names[i].strip(),
                                'amount': ingredient_amounts[i].strip(),
                                'unit': ingredient_units[i]
                            })
                    
                    recipe.ingredients = ingredients
                    
                    # Подготовка шагов приготовления
                    cooking_steps = [step.strip() for step in request.POST.getlist('cooking_step[]') if step.strip()]
                    recipe.cooking_steps = cooking_steps
                    
                    recipe.save()
                    
                    # Сохраняем категории
                    RecipeCategory.objects.filter(recipe=recipe).delete()  # Удаляем старые связи
                    for category_id in request.POST.getlist('categories'):
                        RecipeCategory.objects.create(
                            recipe=recipe,
                            category_id=category_id
                        )
                    
                    messages.success(request, 'Рецепт успешно обновлен!')
                    return redirect('recipe_detail', recipe_id=recipe.id)

            except Exception as e:
                print(f"Error saving recipe: {e}")
                messages.error(request, 'Произошла ошибка при сохранении рецепта')
    else:
        form = RecipeForm(instance=recipe)

    # Получаем текущие категории рецепта через связанную модель
    recipe_categories = RecipeCategory.objects.filter(recipe=recipe)
    selected_category_ids = [rc.category_id for rc in recipe_categories]

    context = {
        'form': form,
        'recipe': recipe,
        'categories': Category.objects.all(),
        'selected_categories': selected_category_ids,
        'units': UnitChoices.choices,
    }
    
    return render(request, 'myapp/edit_recipe.html', context)



@login_required
def delete_recipe(request, recipe_id):
    """Удаление рецепта."""
    recipe = get_object_or_404(Recipe, id=recipe_id, author=request.user)

    if request.method == 'POST':
        try:
            # Сначала удаляем связи с категориями
            RecipeCategory.objects.filter(recipe=recipe).delete()
            # Затем удаляем сам рецепт
            recipe.delete()
            messages.success(request, 'Рецепт успешно удален!')
            return redirect('my_recipes')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении рецепта: {str(e)}')
            return redirect('recipe_detail', recipe_id=recipe_id)
    
    return render(request, 'myapp/delete_recipe.html', {'recipe': recipe})

def recipe_detail(request, recipe_id):
    """Детальный просмотр рецепта."""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe_categories = RecipeCategory.objects.filter(recipe=recipe).select_related('category')
    
    context = {
        'recipe': recipe,
        'categories': recipe_categories,
    }
    return render(request, 'myapp/recipe_detail.html', context)

def blog(request):
    return render(request, 'myapp/blog.html')

def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'myapp/categories.html', {'categories': categories})

def category_recipes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = Recipe.objects.filter(recipecategory__category=category)
    return render(request, 'myapp/category_recipes.html', {
        'category': category,
        'recipes': recipes
    })
