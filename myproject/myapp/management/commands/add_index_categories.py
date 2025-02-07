from django.core.management.base import BaseCommand
from myapp.models import Category

class Command(BaseCommand):
    help = 'Добавляет категории для супов, завтраков, сэндвичей и салатов'

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Супы", "photo": "category_photos/soup_image.png"},
            {"name": "Завтраки", "photo": "category_photos/breakfast_image.png"},
            {"name": "Сэндвичи", "photo": "category_photos/sandwich_image.png"},
            {"name": "Салаты", "photo": "category_photos/salad_image.png"}
        ]

        for category in categories:
            Category.objects.get_or_create(name=category['name'], photo=category['photo'])

        self.stdout.write(self.style.SUCCESS('Категории успешно добавлены!'))
