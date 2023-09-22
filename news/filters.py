from django.forms import DateInput
from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter, DateTimeFilter, TypedMultipleChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='заголовок содержит',
    )
    categories = ModelMultipleChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='категория',
    )
    dateCreation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
        label='дата публикации после',
    )


class CategoryTypeFilter(FilterSet):
    cType = TypedMultipleChoiceFilter(
        field_name='categoryType',
        choices=Post.CATEGORY_CHOICES,
        label='тип публикации',
    )
