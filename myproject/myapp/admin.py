from django.contrib import admin
from .models import Recipe, Category, RecipeCategory

admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
