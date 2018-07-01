import html
from .escaped_characters import escaped_characters

def html_escape(text):
    text = html.escape(text)
    for character, escape_code in escaped_characters.items():
        text = text.replace(character, escape_code)
    return text
