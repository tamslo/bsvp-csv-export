from ..utils.html_escape import html_escape
from modules.parser.download import parse_download
from modules.logger import Logger

def build_download(prod_fields, download_field):
    download = ""
    if download_field in prod_fields:
        download_content = parse_download(prod_fields[download_field], prod_fields["ARTNR"])

        if download_content == None:
            return download

        download_name = html_escape(
            "{} - {}".format(download_content["type"], download_content["product"])
        )
        download += '<a href="{}" target="_blank">'.format(download_content["path"])
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
