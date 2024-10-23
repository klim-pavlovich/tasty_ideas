from myapp.models import Recipe, Category, RecipeCategory
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete data in DB."

    def handle(self, *args, **kwargs):
        # Удаляем все рецепты
        Recipe.objects.all().delete()

        # Удаляем все категории
        Category.objects.all().delete()

        # Удаляем все записи в связующей таблице, если нужно
        RecipeCategory.objects.all().delete()
