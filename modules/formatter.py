# -*- coding: utf-8 -*-
import html

# TODO map and functions
# TODO validate format
# TODO call from main
# TODO refactor (mainly remove and rename) build_cofigs in exporter
formatters = {
    "wahrheitswert_englisch": lamba x: x,

}

def format_value(format_options, name, value):
    value = html.unescape(value).strip()
    # TODO read option from config
    return value
