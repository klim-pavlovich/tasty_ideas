from random import choices

from django.core.management.base import BaseCommand
from myapp.models import Recipe, Category, RecipeCategory, User

LOREM = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Earum error velit, aut asperiores ' \
        'laudantium non repudiandae perspiciatis delectus eveniet, alias excepturi accusantium ' \
        'doloremque dolores, corrupti consequuntur quo fugiat qui vero quos quasi nobis facilis provident ' \
        'quaerat tenetur? Iure sunt, quisquam officia itaque tempore neque a dolorem odit aspernatur, commodi ' \
        'exercitationem quidem debitis eveniet incidunt sint asperiores esse laborum. Soluta pariatur expedita ' \
        'eos sunt non. Nihil dolorum quisquam assumenda laboriosam voluptatum, laudantium possimus iste cum cumque ' \
        'consectetur aperiam molestias magni fugiat et, delectus deserunt ipsum? Saepe molestiae dolor dignissimos ' \
        'sint dolorem rem reiciendis minus soluta laborum incidunt, esse adipisci eaque ut corporis in deleniti'


class Command(BaseCommand):
    help = "Generate fake categories and recipes."

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Categories number')

    def handle(self, *args, **kwargs):
        text = LOREM.split()
        count = kwargs.get('count')

        # Получаем первого пользователя или создаем нового
        author = User.objects.first()
        if author is None:
            author = User.objects.create_user(username='default_user', password='password123')

        for i in range(1, count+1):
            category = Category(
                name=f'Name{i}',
                description=" ".join(choices(text, k=64))
                )
            category.save()
            for j in range(1, count + 1):
                recipe = Recipe(
                    title=f'Title-{j}',
                    description=" ".join(choices(text, k=64)),
                    coocking_steps=" ".join(choices(text, k=64)),
                    coocking_time=30,
                    author=author,
                    ingredients=" ".join(choices(text, k=64)),
                )
                recipe.save()

                RecipeCategory.objects.create(recipe=recipe, category=category)