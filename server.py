from flask import Flask, render_template, json, request, redirect, url_for
from flask_cors import CORS

from modules.runner import Runner

app = Flask(__name__)
CORS(app)
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
    runner.add_task(exporter, manufacturers)
    return json.dumps(runner.get_exporters());

if __name__ == "__main__":
    app.env = "development"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
