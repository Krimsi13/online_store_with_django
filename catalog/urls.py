from django.urls import path

from catalog.views import index, contacts, product

app_name = 'catalog'

urlpatterns = [
    path('', index),
    path('contacts/', contacts),
    path('product/<int:pk>', product, name='product'),
]
