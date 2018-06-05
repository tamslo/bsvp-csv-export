import json, os, shutil

def archive_exports(general_config_file):
    with open(general_config_file, "r", encoding="utf-8") as config_file:
        general_config = json.load(config_file)
        output_directory = general_config["export-ordner"]
        archive_name = "Archiv"
        archive_directory = output_directory + archive_name

        # Ausführung anhalten, wenn es noch keine Exports gibt
        if not os.path.isdir(output_directory): return None

        # Wenn es bereits Dateien im Output-Verzeichnis gibt, werden diese
        # archiviert. Entweder gibt es schon einen Archiv-Ordner, der gelöscht
        # und neu angelegt wird, oder der Ornder wird erstellt. Dann werden die
        # vorhandenen Dateien in den Ordner kopiert.
        if len(os.listdir(output_directory)) != 0:
            if os.path.exists(archive_directory):
                shutil.rmtree(archive_directory)
            os.makedirs(archive_directory)

            for file in os.listdir(output_directory):
                if file != archive_name:
                    current_path = "{}/{}".format(output_directory, file)
                    new_path = "{}/{}".format(archive_directory, file)
                    shutil.move(current_path, new_path)
