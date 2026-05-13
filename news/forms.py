from django import forms
from django.core.exceptions import ValidationError
from .models import Post

# Добавляем нужные импорты для регистрации
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

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


# НОВАЯ ФОРМА ДЛЯ РЕГИСТРАЦИИ
class BasicSignupForm(SignupForm):

    def save(self, request):
        # Сохраняем пользователя, как это делает стандартная форма allauth
        user = super(BasicSignupForm, self).save(request)
        # Находим группу common
        basic_group = Group.objects.get(name='common')
        # Добавляем пользователя в группу
        basic_group.user_set.add(user)
        return user
