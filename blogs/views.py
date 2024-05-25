from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blogs.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ("title", "content", "preview",)
    success_url = reverse_lazy("blogs:blog_list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Блоги'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ("title", "content", "preview", "is_published",)

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blogs:blog_view", args=[self.kwargs.get("pk")])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy("blogs:blog_list")
