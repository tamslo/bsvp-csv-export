def export_shipping(parameters):
    prod_fields = parameters["prod_fields"]
    if not "DELSTAT" in prod_fields:
        return None
    del_stat = prod_fields["DELSTAT"]
    try:
        num_del_stat = int(del_stat)
    except (ValueError, TypeError):
        return None
    return str(num_del_stat + 1)
