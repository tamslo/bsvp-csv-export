from ..html_escape import html_escape

download_prefix = "media/Links/"

def build_download_path(path):
    if path.startswith(download_prefix):
        return path
    else:
        return download_prefix + path

def build_download(prod_fields, download_field):
    download = ""
    if download_field in prod_fields:
        download_content = prod_fields[download_field]
        download_parts = download_content.split("][")

        if (len(download_parts) != 5):
            warning_text = "[ACHTUNG] Unbekanntes Download-Format von "
            warning_text += download_field
            warning_text += " in PROD Datei des Produkts mit der Artikelnummer"
            warning_text += prod_fields["ARTNR"]
            warning_text += " von " + prod_fields["MANUFACTURER"]
            warning_text += ". Der Download wird übersprungen."
            print(warning_text)
            return download

        download_path = build_download_path(download_parts[0]).strip()
        product_name = download_parts[1].strip()
        download_type = download_parts[2].strip()
        download_name = html_escape(
            "{} - {}".format(download_type, product_name)
        )

        download += '<a href="{}" target="_blank">'.format(download_path)
        download += '<img title="Download {}" '.format(download_name)
        download += 'alt="Download" src="/images/download.jpg" '
        download += 'style="vertical-align: middle;">'
        download += "</a>"
        download += download_name
        download += "<br>"

    return download

def export_downloads(prod_fields, ilugg_fields):
    downloads = "<p>"
    max_downloads = int(ilugg_fields["DownCount"])
    index = 0

    while index < max_downloads:
        download_field = "DOWNLOAD." + str(index)
        downloads += build_download(prod_fields, download_field)
        index += 1

    downloads += "</p>"
    return downloads
