from flask import Flask, render_template, json, request, redirect, url_for
from flask_cors import CORS

from modules.runner import Runner

app = Flask(__name__)
CORS(app)
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

@app.route("/manufacturers", methods=["GET"])
def manufacturers():
    return json.dumps(list(runner.manufacturers.keys()))

@app.route("/exporters", methods=["GET"])
def exporters():
    return json.dumps(prepare_exporters(runner.exporters))

@app.route("/run", methods=["GET"])
def run():
    exporter = request.args.get("exporter")
    manufacturers = request.args.get("manufacturers").split(",")
    runner.run(exporter, manufacturers)
    return json.dumps(prepare_exporters(runner.exporters));

if __name__ == "__main__":
    app.env = "development"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
