from .general import export_general_description
from .details import export_details
from .downloads import export_downloads

def export_description(parameters):
    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]

    description = "<!--description-->"
    description += export_general_description()
    description += "<!--/description-->"
    description += "<!--details-->"
    description += export_details()
    description += "<!--/details-->"
    description += "<!--downloads-->"
    description += export_downloads(prod_fields, ilugg_fields)
    description += "<!--/downloads-->"
    return description
