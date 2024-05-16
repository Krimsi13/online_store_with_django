from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='product/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price_per_purchase = models.IntegerField(default=0, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    # manufactured_at = models.DateTimeField(**NULLABLE, verbose_name='Дата производства продукта')

    owner = models.ForeignKey(User, verbose_name="Владелец", help_text="Укажите владельца", **NULLABLE,
                              on_delete=models.SET_NULL)

    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_edit_description_product", "Can edit description product"),
            ("can_edit_category_product", "Can edit category product")
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='versions')
    number = models.IntegerField(verbose_name='Номер версии')
    name = models.TextField(**NULLABLE, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Текущая версия')

    def __str__(self):
        return f'{self.product} {self.number} {self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
