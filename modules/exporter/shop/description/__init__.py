from .general import export_general_description
from .details import export_details
from .downloads import export_downloads
from modules.constants import TECHDATA

def unescape_bsvp(text, prod_fields):
    text = text.replace("$Artikelname$", prod_fields["NAME"])
    text = text.replace("$Artikelnumber$", prod_fields["ARTNR"])
    text = text.replace("$LP$", prod_fields["PRICE"])
    return text

def export_description(parameters):
    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]

    description = "<!--description-->"
    description += export_general_description(parameters)
    description += "<!--/description-->"
    description += "<!--details-->"
    if (TECHDATA in prod_fields and prod_fields[TECHDATA]):
        description += export_details(parameters)
    description += "<!--/details-->"
    description += "<!--downloads-->"
    description += export_downloads(prod_fields, ilugg_fields)
    description += "<!--/downloads-->"
    return unescape_bsvp(description, prod_fields)
