from flask import Flask, jsonify, redirect
from flask_cors import cross_origin, CORS
from util.underground import underground, planned_closures
from util.bikes import bikes

app = Flask(__name__)
CORS().init_app(app, resources={r"*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
@cross_origin(origins="*")
def root():
    return redirect("https://github.com/cxllm/tfl-status-api#tfl-status-api")


@app.route("/underground")
@cross_origin(origins="*")
def underground_route():
    return jsonify(
        {"current_status": underground(), "weekend_closures": planned_closures()}
    )


@app.route("/bikes")
@cross_origin(origins="*")
def bike_route():
    return jsonify(bikes())


if __name__ == "__main__":
    app.run(debug=True)
