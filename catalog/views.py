from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'Главная'
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        products = Product.objects.all()

        for product in products:
            versions = Version.objects.filter(product=product)
            active_versions = versions.filter(is_current=True)
            if active_versions:
                product.name_version = active_versions.last().name
                product.number_version = active_versions.last().number
        context_data['object_list'] = products
        return context_data


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


class ProductDetailView(DetailView, LoginRequiredMixin):
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

class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:index')

    def _get_version_formset(self):
        version_formset = inlineformset_factory(
            parent_model=self.model,
            model=Version,
            form=VersionForm,
            extra=1
        )

        if self.request.method == 'POST':
            return version_formset(self.request.POST, instance=self.object)
        else:
            return version_formset(instance=self.object)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['formset'] = self._get_version_formset()
        return context_data

    def form_valid(self, form: ProductForm):

        context = self.get_context_data()
        versions_formset = context.get('formset')

        self.object = form.save()

        if versions_formset and versions_formset.is_valid():
            versions_formset.instance = self.object
            versions_formset.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView, LoginRequiredMixin):
    model = Product
    success_url = reverse_lazy('catalog:index')
