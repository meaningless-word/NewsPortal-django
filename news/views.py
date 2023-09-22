from datetime import datetime

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Post, Author
from .filters import PostFilter, CategoryTypeFilter
from .forms import PostForm


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
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = CategoryTypeFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

class PostSearchView(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class NewsPostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    categoryType = 'NW'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cType'] = dict(Post.CATEGORY_CHOICES)[self.categoryType]
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = self.categoryType
        post.author = Author.objects.first()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlePostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    categoryType = 'AR'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cType'] = dict(Post.CATEGORY_CHOICES)[self.categoryType]
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = self.categoryType
        post.author = Author.objects.first()
        return super().form_valid(form)
