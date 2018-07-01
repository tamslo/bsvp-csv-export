from .table import Table
from .get_techdata_value import get_value

def should_build_table(prod_fields):
    if "ENERGYCLASS" in prod_fields:
        return prod_fields["ENERGYCLASS"] != ""

def export_energy_efficiency_text(parameters):
    prod_fields = parameters["prod_fields"]
    attribute_names = parameters["attribute_names"]
    tooltips = parameters["tooltips"]
    rows = parameters["specification"]["fields"]
    techdata = prod_fields["TECHDATA"]
    table = Table(tooltips)

    if should_build_table(prod_fields):
        table.make_header(get_value(attribute_names, "0000012", warn=True))
        for field_id in rows:
            field_name = get_value(attribute_names, field_id, warn=True)
            table.make_row(
                field_name,
                get_value(techdata, field_id)
            )
        return table.to_string()
