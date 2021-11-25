from modules.logger import Logger

logger = Logger()

def grouping(value, format_option):
    try:
        numeric_value = float(value.replace(",", "."))
        matching_threshold = None
        group_thresholds = format_option["thresholds"]
        largest_threshold = max(group_thresholds)
        digits = len(str(largest_threshold))
        for threshold in group_thresholds:
            if numeric_value <= threshold:
                matching_threshold = threshold
                break

        if matching_threshold != None:
             indicator = "bis"
        else:
            indicator = "über"
            matching_threshold = largest_threshold

        unit = format_option["unit"]
        return "{} {}{}".format(indicator, str(matching_threshold).zfill(digits), unit)
    except:
        logger.log("Der Wert '{}' kann nicht gruppiert werden, da er nicht numerisch ist.".format(value))
        return value