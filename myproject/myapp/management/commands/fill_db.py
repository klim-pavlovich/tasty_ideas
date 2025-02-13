from random import choices, randint
from django.core.management.base import BaseCommand
from myapp.models import Recipe, Category, RecipeCategory, User, UnitChoices
from django.core.files import File
import os
from django.conf import settings
from pathlib import Path

LOREM = 'Lorem ipsum dolor sit amet consectetur adipisicing elit...'

class Command(BaseCommand):
    help = "Генерирует фейковые категории и рецепты."

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Categories number')

    def get_test_image(self):
        """Получает путь к тестовому изображению"""
        # Ищем изображение в каждой директории из STATICFILES_DIRS
        for static_dir in settings.STATICFILES_DIRS:
            image_path = os.path.join(static_dir, 'images', 'test_image.jpg')
            if os.path.exists(image_path):
                return image_path
        
        # Если изображение не найдено, проверяем в STATIC_ROOT
        static_root_path = os.path.join(settings.STATIC_ROOT, 'images', 'test_image.jpg')
        if os.path.exists(static_root_path):
            return static_root_path
        
        raise Exception(
            "Test image not found. Please place test_image.jpg in one of the following locations:\n" +
            "\n".join([
                str(Path(d) / 'images' / 'test_image.jpg') for d in settings.STATICFILES_DIRS
            ])
        )

    def generate_ingredients(self):
        ingredients = []
        for _ in range(randint(2, 5)):
            ingredients.append({
                'name': f'Ингредиент {randint(1, 100)}',
                'amount': randint(1, 1000),
                'unit': choices(UnitChoices.values())[0]
            })
        return ingredients

    def generate_cooking_steps(self):
        steps = []
        for i in range(randint(3, 7)):
            steps.append(f"Шаг {i+1}: " + " ".join(choices(LOREM.split(), k=10)))
        return steps

    def handle(self, *args, **kwargs):
        text = LOREM.split()
        count = kwargs.get('count')
        test_image_path = self.get_test_image()

        # Получаем первого пользователя или создаем нового
        author = User.objects.first()
        if author is None:
            author = User.objects.create_user(
                username='default_user',
                password='password123',
                email='default@example.com'
            )

        for i in range(1, count+1):
            # Создаем категорию
            with open(test_image_path, 'rb') as img_file:
                category = Category(
                    name=f'Категория {i}',
                    description=" ".join(choices(text, k=10)),
                )
                category.photo.save(
                    'test_image.jpg',
                    File(img_file),
                    save=False
                )
                category.save()

            # Создаем рецепты для каждой категории
            for j in range(1, count + 1):
                with open(test_image_path, 'rb') as img_file:
                    recipe = Recipe(
                        title=f'Рецепт {j}',
                        description=" ".join(choices(text, k=20)),
                        cooking_steps=self.generate_cooking_steps(),
                        cooking_time=randint(5, 180),
                        author=author,
                        ingredients=self.generate_ingredients(),
                    )
                    recipe.image_of_food.save(
                        'test_image.jpg',
                        File(img_file),
                        save=False
                    )
                    recipe.save()

                # Создаем связь между рецептом и категорией
                RecipeCategory.objects.create(recipe=recipe, category=category)

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {count} категорий и {count*count} рецептов')
        )