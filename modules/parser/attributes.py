from modules.constants import ATTRIBUTES_PATH

FIELD_SPARATOR = "§+§"

def parse_attributes():
    with open(ATTRIBUTES_PATH, "r") as attributes_file:
        attribute_lines = attributes_file.readlines()
        attributes = {}
        for attribute_line in attribute_lines:
            attribute_properties = attribute_line.split(FIELD_SPARATOR)
            attribute_id = attribute_properties[0].strip()
            attribute_name = attribute_properties[1].strip()
            if attribute_name != "":
                attribute_name = attribute_properties[1].strip()
            else:
                continue
            attributes[attribute_id] = attribute_name
        return attributes
