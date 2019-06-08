from .escaped_characters import escaped_characters

def unescape_bsvp_to_html(text):
    def replacement(character, html_escape_code):
        return html_escape_code
    return unescape(text, replacement)

def unescape_bsvp_to_text(text):
    def replacement(character, html_escape_code):
        return character
    return unescape(text, replacement)

def unescape(text, replacement):
    text = text.replace("&EOL", "")
    for character, html_escape_code in escaped_characters.items():
        bsvp_escape_code = character + "&SM"
        other_bsvp_escape_code = html_escape_code.replace(";", "&SM")
        text = text.replace(bsvp_escape_code, replacement(character, html_escape_code))
        text = text.replace(other_bsvp_escape_code, replacement(character, html_escape_code))
    return text
