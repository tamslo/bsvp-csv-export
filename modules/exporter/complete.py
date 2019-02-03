# Ideen für Implementierung

# Alle möglichen Felder sammeln (sollte vorm Export geschehen sein)

general_data_fields = set()
tech_data_fields = set()

for product in all_products
    if do_complete_export:
        for field_name, field_value in fields.items():
            if field_name != "TECHDATA":
                general_data_fields.add(field_name)
            else:
                for field_id in field_value.keys():
                    tech_data_fields.add(field_id)

if do_complete_export:
    general_data_fields = sorted(general_data_fields)
    tech_data_fields = sorted(tech_data_fields)

# Im Export alle Felder in CSV pro Hersteller schreiben (TECHDATA Felder z.B. als TECHDATA.0000191)
