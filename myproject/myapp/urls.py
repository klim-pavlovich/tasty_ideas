from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index_recipes, name='index_recipes'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.register, name='registration'),
    path('random_recipes/', views.get_five_random_recipes, name='random_recipes'),
    path('detailed_recipe/', views.get_detailed_recipe, name='detailed_recipe'),
    path('recipes_page/', views.recipes_page, name='recipes_page'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('categories/', views.categories, name='categories'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('blog/', views.blog, name='blog'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)