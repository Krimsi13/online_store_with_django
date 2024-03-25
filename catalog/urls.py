from django.urls import path

from catalog.views import index, contacts

app_name = 'catalog'

urlpatterns = [
    path('', index),
    path('contacts/', contacts)
]
