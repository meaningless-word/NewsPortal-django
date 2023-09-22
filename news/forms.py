from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    text = forms.CharField(
        label="содержимое",
        min_length=20,
        widget=forms.Textarea()
    )
    categories = forms.ModelMultipleChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'categories',
        ]

    def clean(self):
        cleaned_data = super().clean()
        t = cleaned_data.get('text')
        if t is not None and len(t) < 22:
            raise ValidationError({
                "text": "Чёт прям коротюсенько..."
            })
        return cleaned_data
