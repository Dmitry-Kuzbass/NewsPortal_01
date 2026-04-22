from django import template

register = template.Library()

# Список нежелательных слов (можно дополнять)
OBSCENE_WORDS = [
    'реклама',
    'редиска',
    'плохоеслово',
    'правила',
    'образования'
]


@register.filter()
def censor(value):
    """
    Фильтр для цензурирования текста.
    Заменяет буквы нежелательных слов на '*'
    """
    # Проверка: является ли значение строкой
    if not isinstance(value, str):
        raise ValueError("Фильтр censor можно применять только к строкам")

    text = value
    for word in OBSCENE_WORDS:
        # Ищем слово в тексте (без учета регистра)
        # Для простоты заменяем слово целиком, сохраняя первую букву
        censored_word = word[0] + '*' * (len(word) - 1)

        # Заменяем во всем тексте
        text = text.replace(word, censored_word)
        # Также проверяем версию с большой буквы
        text = text.replace(word.capitalize(), censored_word.capitalize())

    return text