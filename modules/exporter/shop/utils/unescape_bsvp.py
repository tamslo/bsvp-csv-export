from .escaped_characters import escaped_characters

def unescape_bsvp(text, prod_fields):
    text = text.replace("$Artikelname$", prod_fields["NAME"])
    text = text.replace("$Artikelnumber$", prod_fields["ARTNR"])
    text = text.replace("$LP$", prod_fields["PRICE"])

    for character, escape_code in escaped_characters.items():
        bsvp_escape_code = character + "&SM"
        other_bsvp_escape_code = escape_code.replace(";", "&SM")
        text = text.replace(bsvp_escape_code, escape_code)
        text = text.replace(other_bsvp_escape_code, escape_code)

    text = text.replace("&EOL", "")

    return text
