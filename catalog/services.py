from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Получает данные по продуктам из кэша; если кэш пуст, то получает из БД"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'products_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_category_from_cache():
    """Получает данные по продуктам из кэша; если кэш пуст, то получает из БД"""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'category_list'
    category = cache.get(key)
    if category is not None:
        return category
    products = Category.objects.all()
    cache.set(key, products)
    return category
