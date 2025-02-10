from django import template
from myapp.models import UnitChoices

register = template.Library()  # Регистрируем нашу библиотеку тегов

@register.simple_tag
def get_unit_choices():
    """
    Тег, возвращающий список единиц измерения
    Использование в шаблоне: {% get_unit_choices as units %}
    """
    return UnitChoices.choices()

# Пример дополнительного тега
@register.filter
def unit_exists(value):
    """
    Фильтр, проверяющий существование единицы измерения
    Использование в шаблоне: {{ unit_value|unit_exists }}
    """
    return value in UnitChoices.values()