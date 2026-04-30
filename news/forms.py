from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            # Добавьте другие поля, если они есть в вашей модели Post
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")

        # Проверка на минимальное количество символов (как в задании)
        if text is not None and len(text) < 20:
            raise ValidationError({
                "text": "Текст статьи не может быть менее 20 символов."
            })

        return cleaned_data