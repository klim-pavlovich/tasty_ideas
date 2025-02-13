from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from enum import Enum


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(max_length=250)
    photo = models.ImageField(upload_to='category_photos/', default='default_image.png')
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class UnitChoices(str, Enum):
    GRAM = 'г'
    MILLILITER = 'мл'
    PIECE = 'шт'
    TABLESPOON = 'ст.л.'
    TEASPOON = 'ч.л.'
    KILOGRAM = 'кг'
    LITER = 'л'

    @classmethod
    def choices(cls):
        return [(item.value, item.value) for item in cls]

    @classmethod
    def values(cls):
        return [item.value for item in cls]


class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название блюда")
    description = models.TextField(max_length=5000, verbose_name="Описание")
    cooking_steps = models.JSONField(default=list, verbose_name="Шаги приготовления")
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1440)], verbose_name="Время приготовления (в минутах)")
    image_of_food = models.ImageField(upload_to='recipes_photos', verbose_name="Фото готового блюда")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    ingredients = models.JSONField(default=list, verbose_name="Ингредиенты")
    date_of_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Название: {self.title}, автор: {self.author}, дата создания: {self.date_of_create}"

    def clean_ingredients(self):
        """Валидация единиц измерения в ингредиентах"""
        for ingredient in self.ingredients:
            if ingredient.get('unit') not in UnitChoices.values():
                raise ValidationError(f"Недопустимая единица измерения: {ingredient.get('unit')}")

    @property
    def total_quantity_time(self):
        """Подсчет общего количества времени приготовления всех рецептов через sum()."""
        return sum(recipe.cooking_time for recipe in Recipe.objects.all())

class RecipeCategory(models.Model):
    # Убрал связь M-to-M в Рецептах, так как в задании указано, что нужно написать модель.
    # Если оставить, то будут дублироваться данные.
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Рецепт: {self.recipe.title}, категория: {self.category.name}'