def replacement(value, format_option):
    before_values = format_option["before"]
    afterwards_value = format_option["afterwards"]
    option = format_option["option"]
    if option == "startswith":
        for before_value in before_values:
            if value.startswith(before_value):
                value = value.replace(before_value, afterwards_value)
                break
    elif option == "endswith":
        for before_value in before_values:
            if value.endswith(before_value):
                value = value.replace(before_value, afterwards_value)
                break
    else:
        lower_before_values = list(map(
            lambda value: value.lower(),
            before_values
        ))
        if value.lower() in lower_before_values:
            value = afterwards_value
    return value