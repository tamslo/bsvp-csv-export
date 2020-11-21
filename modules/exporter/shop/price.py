import math

def finalize_price(price):
    return str(math.floor(price))

def get_catalog_price(prod_fields):
    price = prod_fields["PRICE"]
    if ("," in price):
        if ("." in price):
            price = price.replace(",", "")
        else:
            price = price.replace(",", ".")
    price = int(price)
    return price

def get_purchasing_price(prod_fields):
    catalog_price = get_catalog_price(prod_fields)
    discount = float(prod_fields["RABATT"].split(":")[1])
    purchasing_price = catalog_price * discount
    return purchasing_price

def export_price(parameters):
    prod_fields = parameters["prod_fields"]
    price_base = prod_fields["PRICEBASE"]
    user_factor = float(prod_fields["USERFAKTVK"].split(":")[1])
    base_price = None
    if price_base == "NettoPrice":
        base_price = get_purchasing_price(prod_fields)
    elif price_base == "ListPrice":
        base_price = get_catalog_price(prod_fields)
    else:
        print("UNKNOWN PRICEBASE: {}".format(price_base))
    price = finalize_price(base_price * user_factor)
    return price

def export_min_price(parameters):
    def get_min_price_factor(ilugg_fields, purchasing_price):
        factor_definition = ilugg_fields["MinPriceFormular"]
        # IF ($EK<threshold) THEN ($EK*greater_factor) ELSE ($EK*smaller_factor)
        split_character = " "
        factor_definition_parts = factor_definition.replace("IF ($EK<", "")
        factor_definition_parts = factor_definition_parts.replace(") THEN ($EK*", split_character)
        factor_definition_parts = factor_definition_parts.replace(") ELSE ($EK*", split_character)
        factor_definition_parts = factor_definition_parts.replace(")", "")
        values = factor_definition_parts.split(split_character)
        threshold = float(values[0])
        greater_factor = float(values[1])
        smaller_factor = float(values[2])
        if (purchasing_price < threshold):
            min_price_factor = greater_factor
        else:
            min_price_factor = smaller_factor
        return min_price_factor

    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]
    purchasing_price = get_purchasing_price(prod_fields)
    min_price_factor = get_min_price_factor(ilugg_fields, purchasing_price)
    min_price = finalize_price(purchasing_price * min_price_factor)
    return min_price
