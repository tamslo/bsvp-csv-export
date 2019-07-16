import json
import os
from modules.logger import Logger
from modules.constants import GENERAL_CONFIG_FILE

def build_download_path(path):
    old_download_prefix = "media/Links/"
    with open(GENERAL_CONFIG_FILE, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        download_prefix = config["downloads-path"]

    # Der Download Pfad beginnt entweder mit dem alten Download Pfad oder mit
    # gar keinem
    if path.startswith(old_download_prefix):
        path = path.replace(old_download_prefix, "")

    return os.path.join(download_prefix, path)

def parse_download(download_content, download_field = None, article = None):
    download_parts = download_content.split("][")
    if (len(download_parts) < 3):
        warning_text = "[ACHTUNG] Unbekanntes Download-Format "
        if download_field != None and article != None:
            warning_text += "von "
            warning_text += download_field
            warning_text += " in "
            warning_text += article
        else:
            warning_text += "({})".format(download_content)
        warning_text += ". Der Download wird übersprungen."
        Logger().log(warning_text)
        return None

    return {
        "path": build_download_path(download_parts[0]).strip(),
        "product": download_parts[1].strip(),
        "type": download_parts[2].strip()
    }
