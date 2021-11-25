def range_from_zero(value, format_option):
    try:
        float(value)
    except:
        pass
    return "0|" + value