import os
from modules.logger import Logger

def build_download_path(path):
    old_download_prefix = "media/Links"
    download_prefix = "media/Links" # TODO: get from config

    if path.startswith(old_download_prefix):
        return path.replace(old_download_prefix, download_prefix)
    else:
        return os.path.join(download_prefix, path)

def parse_download(download_content, article = None):
    download_parts = download_content.split("][")

    if (len(download_parts) < 3):
        if article != None:
            warning_text = "[ACHTUNG] Unbekanntes Download-Format von "
            warning_text += download_field
            warning_text += " in "
            warning_text += article
            warning_text += ". Der Download wird übersprungen."
            Logger().log(warning_text)
        return None

    return {
        "path": build_download_path(download_parts[0]).strip(),
        "product": download_parts[1].strip(),
        "type": download_parts[2].strip()
    }
