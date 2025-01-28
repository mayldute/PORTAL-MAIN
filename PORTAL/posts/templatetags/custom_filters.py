from django import template
import re

register = template.Library()

@register.filter()
def censor(value):
    unwanted_words = ['блять', 'ебать', 'пизда', 'сука', 'хуй']  # Список нежелательных слов для цензуры
    
    for word in unwanted_words:
        value = re.sub(r'\b{}\b'.format(word), '*' * len(word), value, flags=re.IGNORECASE)
        
    return f'{value}'