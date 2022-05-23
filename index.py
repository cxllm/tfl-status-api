import json
from flask import Flask, jsonify, redirect
from util.underground import underground, planned_closures
from util.bikes import bikes

app = Flask(__name__)


@app.route("/")
def root():
    return redirect("https://github.com/cxllm/tfl-status-api#tfl-status-api")


@app.route("/underground")
def underground_route():
    return jsonify(
        {"current_status": underground(), "weekend_closures": planned_closures()}
    )


@app.route("/bikes")
def bike_route():
    return jsonify(bikes())


if __name__ == "__main__":
    app.run(debug=True)
