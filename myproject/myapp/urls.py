from django.urls import path
from .views import index_recipes
from .views import get_five_random_recipes
from .views import get_detailed_recipe
from .views import register
from .views import create_recipe

urlpatterns = [
    path('', index_recipes, name='index_recipes'),
    path('random_recipes/', get_five_random_recipes, name='random_recipes'),
    path('detailed_recipe/', get_detailed_recipe, name='detailed_recipe'),
    path('registration/', register, name='registration'),
    path('create_recipe/', create_recipe, name='create_recipe'),
]
