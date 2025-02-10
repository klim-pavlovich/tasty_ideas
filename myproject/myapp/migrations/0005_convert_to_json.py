from django.db import migrations
import json

def convert_to_json(apps, schema_editor):
    Recipe = apps.get_model('myapp', 'Recipe')
    for recipe in Recipe.objects.all():
        # Конвертируем cooking_steps
        if isinstance(recipe.cooking_steps, str):
            steps = recipe.cooking_steps.split('\n') if recipe.cooking_steps else []
            recipe.cooking_steps = json.dumps(steps)
        
        # Конвертируем ingredients
        if isinstance(recipe.ingredients, str):
            try:
                # Пробуем распарсить как JSON
                json.loads(recipe.ingredients)
            except:
                # Если не получилось, создаем пустой список
                recipe.ingredients = json.dumps([])
        
        recipe.save()

def reverse_convert(apps, schema_editor):
    Recipe = apps.get_model('myapp', 'Recipe')
    for recipe in Recipe.objects.all():
        if recipe.cooking_steps:
            steps = json.loads(recipe.cooking_steps)
            recipe.cooking_steps = '\n'.join(steps)
        
        recipe.ingredients = '[]'
        recipe.save()

class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0004_alter_category_photo'),
    ]

    operations = [
        migrations.RunPython(convert_to_json, reverse_convert),
    ]