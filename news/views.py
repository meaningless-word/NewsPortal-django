from datetime import datetime

from django.views.generic import ListView, DetailView
from .models import Category, Post


class CategoriesListView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Category
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'name'
    # Указываем имя шаблона, в котором будут все инструкции о том, как именно пользователю будут показаны объекты
    template_name = 'news/categories.html'
    # Это имя списка, в котором будут лежать все объекты. его нужно указывать, чтоб обратиться к списку объектов в html-шаблоне
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    # Модель та же, но отображает отдельный объект
    model = Category
    # Используем другой шаблон
    template_name = 'news/category.html'
    # наименование, через которое будет получен контекст
    context_object_name = 'category'


class PostListView(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'