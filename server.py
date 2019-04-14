#!/usr/bin/env python

from flask import Flask, render_template, json, request, redirect, url_for, \
    send_from_directory
from flask_cors import CORS

from modules.runner import Runner
from modules.validator import validate_setup
from modules.constants import GENERAL_CONFIG_FILE, CONFIGURATOR_NAME, \
    SHOP_NAME

app = Flask(__name__)
CORS(app)

validate_setup(GENERAL_CONFIG_FILE, CONFIGURATOR_NAME, SHOP_NAME)
runner = Runner()

@app.route("/manufacturers", methods=["GET"])
def manufacturers():
    return json.dumps(runner.get_manufacturers())

@app.route("/exporters", methods=["GET"])
def exporters():
    return json.dumps(runner.get_exporters())

@app.route("/run", methods=["GET"])
def run():
    exporter = request.args.get("exporter")
    manufacturers = request.args.get("manufacturers").split(",")
    error_code = runner.add_task(exporter, manufacturers)
    if error_code != None:
        return json.dumps({ "error": True, "code": error_code, "exporters": runner.get_exporters() })
    else:
        return json.dumps(runner.get_exporters());

# Routes for client built with `npm run build`

@app.route("/")
def serve():
    return send_from_directory("client/build/", "index.html")


@app.route("/static/js/<path:path>")
def servejs(path):
    return send_from_directory("client/build/static/js/", path)


@app.route("/favicon.ico")
def servefav():
    return send_from_directory("client/build/", "favicon.png")


@app.route("/static/media/<path:path>")
def servemedia(path):
    return send_from_directory("client/build/static/media/", path)

if __name__ == "__main__":
    app.env = "development"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
