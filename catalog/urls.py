from django.urls import path

from catalog.views import catalog

app_name = 'catalog'

urlpatterns = [
    path('', catalog, name='catalog'),
]
