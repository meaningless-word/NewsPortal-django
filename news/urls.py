from django.urls import path
from .views import (
    PostListView, PostDetailView, PostSearchView, NewsPostCreate, PostUpdateView, PostDeleteView,
    ArticlePostCreate, subscriptions, warning_generator, debug_generator, info_generator,
    critical_generator, error_generator
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('news/create/', NewsPostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
    path('article/create/', ArticlePostCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit', PostUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', PostDeleteView.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('debug/', debug_generator, name='debug_generator'),
    path('info/', info_generator, name='info_generator'),
    path('warning/', warning_generator, name='warning_generator'),
    path('error/', error_generator, name='error_generator'),
    path('critical/', critical_generator, name='critical_generator'),
]
