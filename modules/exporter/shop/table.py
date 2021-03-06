from .utils.html_escape import html_escape
from .utils.include_tooltips import include_tooltips

class Table():
    def __init__(self, tooltips):
        self.tooltips = tooltips
        self.rows = []
        self.content_rows = 0

    def __cell(self, class_string, text="", trailing_space=False):
        appendix = "&nbsp;" if trailing_space else ""
        text = html_escape(text)
        text = include_tooltips(self.tooltips, text)
        return '<td class="{}">{}{}</td>'.format(
            class_string,
            text,
            appendix
        )

    def __row(self, cells):
        return "<tr>{}</tr>".format("".join(cells))

    def make_header(self, title):
        class_string = "kb-THeaderLeft"
        header_row = self.__row([
            self.__cell(class_string, title),
            self.__cell(class_string, "")
        ])
        self.rows.append(header_row)

    def make_row(self, description, value):
        description_cell = self.__cell("kb-Tleft", description, trailing_space=True)
        value_cell = self.__cell("kb-Tright", value)
        row = self.__row([
            description_cell,
            value_cell
        ])
        self.rows.append(row)
        self.content_rows += 1

    def make_empty_row(self):
        class_string = "kb-Tnull"
        row = self.__row([
            self.__cell(class_string),
            self.__cell(class_string)
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

        if self.content_rows > 0:
            rows = "".join(self.rows)
            return "<table {}><tbody>{}</tbody></table>".format(
                table_attributes,
                rows
            )
