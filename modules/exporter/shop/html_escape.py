import html

def html_escape(text):
    text = html.escape(text)
    text = text.replace("ä", "&auml;")
    text = text.replace("ö", "&ouml;")
    text = text.replace("ü", "&uuml;")
    text = text.replace("ß", "&szlig;")
    text = text.replace("Ä", "&Auml;")
    text = text.replace("Ö", "&Ouml;")
    text = text.replace("Ü", "&Uuml;")
    text = text.replace("°", "&deg;")
    return text
