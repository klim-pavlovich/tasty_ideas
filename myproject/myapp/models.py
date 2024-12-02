from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    photo = models.ImageField(upload_to='category_photos/', default='default_image.png')

    def __str__(self):
        return f'Название: {self.name}'


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    cooking_steps = models.TextField(max_length=5000)
    cooking_time = models.IntegerField() # в минутах
    image_of_food = models.ImageField(upload_to='recipes_photos', height_field=None, width_field=None, max_length=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.TextField(max_length=2500, blank=True)
    date_of_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Название: {self.title}, автор: {self.author}, дата создания: {self.date_of_create}"


class RecipeCategory(models.Model):
    # Убрал связь M-to-M в Рецептах, так как в задании указано, что нужно написать модель.
    # Если оставить, то будут дублироваться данные.
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Рецепт: {self.recipe.title}, категория: {self.category.name}'