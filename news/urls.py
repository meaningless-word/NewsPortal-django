from django.urls import path
from .views import PostListView, PostDetailView, PostSearchView, NewsPostCreate, PostUpdateView, PostDeleteView, \
    ArticlePostCreate

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
]