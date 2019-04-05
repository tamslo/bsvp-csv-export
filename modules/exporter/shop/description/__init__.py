from .general import export_general_description
from .details import export_details
from .downloads import export_downloads
from ..utils.unescape_bsvp import unescape_bsvp

def export_description(parameters):
    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]

    description = "<!--description-->"
    description += export_general_description(prod_fields, ilugg_fields)
    description += "<!--/description-->"
    description += "<!--details-->"
    if ("TECHDATA" in prod_fields and prod_fields["TECHDATA"]):
        description += export_details(parameters)
    description += "<!--/details-->"
    description += "<!--downloads-->"
    description += export_downloads(prod_fields, ilugg_fields)
    description += "<!--/downloads-->"
    return unescape_bsvp(description, prod_fields)
