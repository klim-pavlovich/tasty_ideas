from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index_recipes, name='index_recipes'),
    path('random_recipes/', views.get_five_random_recipes, name='random_recipes'),
    path('detailed_recipe/', views.get_detailed_recipe, name='detailed_recipe'),
    path('registration/', views.register, name='registration'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)