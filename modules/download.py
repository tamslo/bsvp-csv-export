import os, zipfile

def zip_result(exporter_id, path):
    zip_path = path + exporter_id + "_result.zip"
    if not os.path.exists(zip_path):
        archive = zipfile.ZipFile(zip_path, "w")
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if file_path != zip_path:
                archive.write(
                    file_path,
                    file
                )
        archive.close()
    return zip_path
