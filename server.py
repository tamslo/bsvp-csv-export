from flask import Flask, render_template, json, request

from modules.runner import Runner

app = Flask(__name__)
runner = Runner()

def prepare_exporters(exporters):
    sendable_exporters = {}
    for exporter_key, exporter_values in exporters.items():
        sendable_exporters[exporter_key] = {
            "name": exporter_values["name"],
            "running": exporter_values["running"],
            "log": exporter_values["log"]
        }
    return sendable_exporters

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        manufacturers = list(runner.manufacturers.keys()),
        exporters = prepare_exporters(runner.exporters)
    )

@app.route("/run", methods=["POST"])
def run():
    exporter = request.json["exporter"]
    manufacturers = request.json["manufacturers"]
    runner.run(exporter, manufacturers)
    return render_template(
        "index.html",
        manufacturers = list(runner.manufacturers.keys()),
        exporters = prepare_exporters(runner.exporters)
    )

if __name__ == "__main__":
    app.env = "development"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
