from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index_recipes, name='index_recipes'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.register, name='registration'),

    path('recipes_page/', views.recipes_page, name='recipes_page'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('delete_recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/', views.get_detailed_recipe, name='recipe_detail'),
    path('get_detailed_recipe/', views.get_detailed_recipe, name='detailed_recipe'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('all_recipes/', views.all_recipes, name='all_recipes'),

    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_recipes, name='category_recipes'),
    path('blog/', views.blog, name='blog'),

    path('five_random_recipes/', views.get_five_random_recipes, name='five_random_recipes'),
    path('random_recipe/', views.get_random_recipe, name='random_recipe'),
    
    path('db/', views.total_in_db, name='db'),
    path('view/', views.total_in_view, name='view'),
    path('template/', views.total_in_template, name='template'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)