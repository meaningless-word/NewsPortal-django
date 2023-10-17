from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
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


class PostListView(LoginRequiredMixin, ListView):
    raise_exception = False
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


class PostDetailView(LoginRequiredMixin, DetailView):
    raise_exception = False
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Post.objects.get(pk=self.kwargs['pk']).categories.all().annotate(
            is_subscribed=Exists(self.request.user.categories.filter(id=OuterRef('pk')))
        )
        context['message'] = ''
        return context

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')
        message = ''

        if action == 'subscribe':
            category.subscribers.add(request.user)
            message = 'Подписка оформлена'
        if action == 'unsubscribe':
            category.subscribers.remove(request.user)
            message = 'Подписка отменена'

        context = {
            'post': Post.objects.get(pk=self.kwargs['pk']),
            'categories': Post.objects.get(pk=self.kwargs['pk']).categories.all().annotate(
                is_subscribed=Exists(self.request.user.categories.filter(id=OuterRef('pk')))
            ),
            'message': message,
        }

        return render(request, self.template_name, context)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)  # кэш похож на словарь и метод get действует так же: забирает значение по ключу, а если его нет, то None

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class NewsPostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
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


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlePostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            category.subscribers.add(request.user)
        if action == 'unsubscribe':
            category.subscribers.remove(request.user)

    categories_with_subscriptions = Category.objects.annotate(
            is_subscribed=Exists(request.user.categories.filter(id=OuterRef('pk')))
        ).order_by('name')

    return render(request, 'news/subscriptions.html', {'categories': categories_with_subscriptions},)