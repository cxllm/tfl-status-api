from flask import Flask, jsonify, redirect
from flask_cors import cross_origin
from util.underground import underground, planned_closures
from util.bikes import bikes

app = Flask(__name__)


@app.route("/")
@cross_origin()
def root():
    return redirect("https://github.com/cxllm/tfl-status-api#tfl-status-api")


@app.route("/underground")
@cross_origin()
def underground_route():
    return jsonify(
        {"current_status": underground(), "weekend_closures": planned_closures()}
    )


@app.route("/bikes")
@cross_origin()
def bike_route():
    return jsonify(bikes())


if __name__ == "__main__":
    app.run(debug=True)
