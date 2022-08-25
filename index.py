from flask import Flask, jsonify, redirect, render_template
from flask_cors import cross_origin, CORS
from util.underground import underground, planned_closures
from util.bikes import bikes

app = Flask(
    __name__,
    template_folder="website/build",
    static_folder="website/build",
    static_url_path="/",
)
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/")
@cross_origin(origins="*")
def root():
    response = redirect("https://github.com/cxllm/tfl-status-api#tfl-status-api")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return render_template("index.html")


@app.route("/underground")
@cross_origin(origins="*")
def underground_route():
    response = jsonify(
        {"current_status": underground(), "weekend_closures": planned_closures()}
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/bikes")
@cross_origin(origins="*")
def bike_route():
    response = jsonify(bikes())
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


if __name__ == "__main__":
    app.run(debug=True)
