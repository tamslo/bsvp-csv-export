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

def cell(class_string, text):
    return '<td class="{}">{}</td>'.format(class_string, html.escape(text))

def header_row(title):
    class_string = "kb-THeaderLeft"
    return row([cell(class_string, title), cell(class_string, "")])
