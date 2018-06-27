import html

def table(rows):
    table_attributes = {
        'class="p_desc-table" '
        'style="'
        "width: 90%;"
        "max-width: 95%;"
        "border-collapse: collapse;"
        "font-family: sans-serif;"
        "-webkit-font-smoothing: antialiased;"
        '"'
    }
    return "<table {}><tbody>{}</tbody></table>".format(table_attributes, rows)

def row(cells):
    return "<tr>{}</tr>".format("".join(cells))

def html_escape(text):
    text = html.escape(text)
    text = text.replace("ä", "&auml;")
    text = text.replace("ö", "&ouml;")
    text = text.replace("ü", "&uuml;")
    text = text.replace("ß", "&szlig;")
    text = text.replace("Ä", "&Auml;")
    text = text.replace("Ö", "&Ouml;")
    text = text.replace("Ü", "&Uuml;")
    return text

def cell(class_string, text, trailing_space=False):
    appendix = "&nbsp;" if trailing_space else ""
    return '<td class="{}">{}{}</td>'.format(
        class_string,
        html_escape(text),
        appendix
    )

def description_cell(text):
    return cell("kb-Tleft", text, trailing_space=True)

def value_cell(text):
    return cell("kb-Tright", text)

def body_row(description, value):
    return row([
        description_cell(description),
        value_cell(value)
    ])

def header_row(title):
    class_string = "kb-THeaderLeft"
    return row([cell(class_string, title), cell(class_string, "")])
