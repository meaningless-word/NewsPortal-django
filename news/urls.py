from django.urls import path
from .views import PostListView, PostDetailView, CategoriesListView, CategoryDetailView

urlpatterns = [
    path('', PostListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view()),
    path('categories/', CategoriesListView.as_view()),
    path('categories/<int:pk>', CategoryDetailView.as_view()),
]