from ..utils.include_tooltips import include_tooltips
from .welcome_text import get_welcome_text

def export_general_description(parameters):
    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]
    tooltips = parameters["tooltips"]
    text = get_welcome_text(prod_fields, ilugg_fields) + prod_fields["DESC"]
    return include_tooltips(tooltips, text)
