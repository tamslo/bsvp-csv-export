from ..table import Table
from ..utils.get_techdata_value import get_value
from modules.constants import TECHDATA

def export_details(parameters):
    prod_fields = parameters["prod_fields"]
    attribute_names = parameters["attribute_names"]
    attribute_types = parameters["attribute_types"]
    tooltips = parameters["tooltips"]
    techdata = prod_fields[TECHDATA]
    table = Table(tooltips)
    for field_id, type in attribute_types.items():
        attribute_name = get_value(attribute_names, field_id, warn=True)
        if type == "HEAD":
            table.make_empty_row()
            table.make_header(attribute_name)
        else:
            attribute_value = get_value(techdata, field_id)
            table.make_row(attribute_name, attribute_value)
    return table.to_string()
