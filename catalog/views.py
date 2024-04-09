from django.shortcuts import render

from catalog.models import Product


def index(request):
    context = {'object_list': Product.objects.all()}
    return render(request, 'catalog/index.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')
    return render(request, 'catalog/contacts.html')


def product(request, pk):
    context = {
        'object': Product.objects.get(pk=pk),
        'title': 'Товар'
    }
    return render(request, 'catalog/product.html', context)
