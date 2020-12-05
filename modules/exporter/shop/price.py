import math
from modules.logger import Logger
from modules.constants import ARTICLE_NUMBER

def finalize_price(price):
    return str(math.floor(price))

def get_number(string):
    if ("," in string):
        if ("." in string):
            string = string.replace(",", "")
        else:
            string = string.replace(",", ".")
    return float(string)


def get_catalog_price(prod_fields):
    return get_number(prod_fields["PRICE"])

def get_factor(prod_fields, prod_field, ilugg_fields, ilugg_field):
    prod_definition = prod_fields[prod_field]
    ilugg_definition = ilugg_fields[ilugg_field]
    factor_category = prod_definition.split(":")[0]
    factor_definitions = ilugg_definition.split("§")
    factor = None
    for factor_definition in factor_definitions:
        if factor_definition.startswith(factor_category):
            if ":" in factor_definition:
                factor = factor_definition.split(":")[1]
            break
    if factor == None:
        logger = Logger()
        factor = prod_definition
        if ":" in factor:
            factor = factor.split(":")[1]
        log_text = "{}: Faktor zur Preisberechnung".format(prod_fields[ARTICLE_NUMBER])
        log_text += " konnte nicht bestimmt werden."
        log_text += " {} in PROD ist '{}',".format(prod_field, prod_definition)
        log_text += " {} in ILUGG ist '{}'.".format(ilugg_field, ilugg_definition)
        log_text += " {} wird als Faktor angenommen.".format(factor)
        logger.log(log_text)
    return get_number(factor)

def get_purchasing_price(prod_fields, ilugg_fields):
    def get_discount(prod_fields, ilugg_fields):
        return get_factor(prod_fields, "RABATT", ilugg_fields, "RABATT")

    catalog_price = get_catalog_price(prod_fields)
    discount = get_discount(prod_fields, ilugg_fields)
    purchasing_price = catalog_price * discount
    return purchasing_price

def export_price(parameters):
    def get_user_factor(prod_fields, ilugg_fields):
        return get_factor(prod_fields, "USERFAKTVK", ilugg_fields, "UFAKTVK")

    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]
    price_base = prod_fields["PRICEBASE"]
    user_factor = get_user_factor(prod_fields, ilugg_fields)
    base_price = None
    if price_base == "NettoPrice":
        base_price = get_purchasing_price(prod_fields, ilugg_fields)
    elif price_base == "ListPrice":
        base_price = get_catalog_price(prod_fields)
    else:
        raise Exception("{}: Unerwartete PRICEBASE '{}'".format(prod_fields[ARTICLE_NUMBER], price_base))
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
        threshold = get_number(values[0])
        greater_factor = get_number(values[1])
        smaller_factor = get_number(values[2])
        if (purchasing_price < threshold):
            min_price_factor = greater_factor
        else:
            min_price_factor = smaller_factor
        return min_price_factor

    prod_fields = parameters["prod_fields"]
    ilugg_fields = parameters["ilugg_fields"]
    purchasing_price = get_purchasing_price(prod_fields, ilugg_fields)
    min_price_factor = get_min_price_factor(ilugg_fields, purchasing_price)
    min_price = finalize_price(purchasing_price * min_price_factor)
    return min_price
