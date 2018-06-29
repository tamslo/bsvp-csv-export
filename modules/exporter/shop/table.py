import html

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

class Table():
    def __init__(self, tooltips):
        self.tooltips = tooltips
        self.header = ""
        self.rows = []

    def __cell(self, class_string, text, trailing_space=False):
        appendix = "&nbsp;" if trailing_space else ""
        return '<td class="{}">{}{}</td>'.format(
            class_string,
            html_escape(text),
            appendix
        )

    def __row(self, cells):
        return "<tr>{}</tr>".format("".join(cells))

    def make_header(self, title):
        class_string = "kb-THeaderLeft"
        self.header = self.__row([
            self.__cell(class_string, title),
            self.__cell(class_string, "")
        ])

    def make_row(self, description, value):
        description_cell = self.__cell("kb-Tleft", description, trailing_space=True)
        value_cell = self.__cell("kb-Tright", value)
        row = self.__row([
            description_cell,
            value_cell
        ])
        self.rows.append(row)

    def to_string(self):
        table_attributes = 'class="p_desc-table" '
        table_attributes += 'style="'
        table_attributes += "width: 90%;"
        table_attributes += "max-width: 95%;"
        table_attributes += "border-collapse: collapse;"
        table_attributes += "font-family: sans-serif;"
        table_attributes += "-webkit-font-smoothing: antialiased;"
        table_attributes += '"'

        if len(self.rows) > 0:
            rows = self.header + "".join(self.rows)
            return "<table {}><tbody>{}</tbody></table>".format(
                table_attributes,
                rows
            )
