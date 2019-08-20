import re
from .html_escape import html_escape

def include_tooltips(tooltips, text):
    # Erstetze Begriffe im Text die durch Tooltips ergänzt werden sollen
    # erst durch Platzhalter, damit Begriffe in Tooltips nicht ersetzt
    # werden
    tooltip_placeholders = {}

    for tooltip_key, tooltip_value in tooltips.items():
        tooltip_key = html_escape(tooltip_key)
        if re.search(r'\b' + re.escape(tooltip_key) + r'\b', text):
            tooltip = '<span class="kb-tooltip" title="'
            tooltip += html_escape(tooltip_value)
            tooltip += '">'
            tooltip += tooltip_key
            tooltip += "</span>"

            tooltip_placeholder = "$${}$$".format(tooltip_key)
            tooltip_placeholders[tooltip_placeholder] = tooltip
            text = text.replace(tooltip_key, tooltip_placeholder)

    for placeholder, tooltip in tooltip_placeholders.items():
        text = text.replace(placeholder, tooltip)

    return text
