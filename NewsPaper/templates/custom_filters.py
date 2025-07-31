from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    bad_words = ['казино', 'ставки', 'негодяй', 'фикалии', 'фунчоза']  # Добавьте нежелательные слова
    replacement = '*' * 3  # заменить на три звездочки
    result = value
    for word in bad_words:
        result = result.replace(word, replacement)
    return result
