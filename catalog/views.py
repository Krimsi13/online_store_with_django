from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Главная'
    }


# def index(request):
#     context = {'object_list': Product.objects.all(),
#                'title': 'Главная'}
#     return render(request, 'catalog/index.html', context)


class ContactsPageView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты'
    }

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f'{name} ({phone}): {message}')
        return render(request, 'catalog/contacts.html', context=self.extra_context)


# def contacts(request):
#     context = {'title': 'Контакты'}
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'{name} ({phone}): {message}')
#     return render(request, 'catalog/contacts.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    extra_context = {
        'title': 'Описание продукта'
    }


# def product(request, pk):
#     context = {
#         'object': Product.objects.get(pk=pk),
#         'title': 'Товар'
#     }
#     return render(request, 'catalog/product.html', context)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:index')
