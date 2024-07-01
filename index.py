import re
from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import cross_origin, CORS
from util.underground import underground, planned_closures
from util.bikes import bikes
from util.maps import get_coordinates, get_distance_between

app = Flask(
    __name__,
    template_folder="website/build",
    static_folder="website/build",
    static_url_path="/",
)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type"],
            "supports_credentials": True,
        }
    },
)

app.config["CORS_HEADERS"] = "Content-Type"


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


@app.route("/")
def root():
    return render_template("index.html")


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


@app.route("/bikes/closest-stations")
@cross_origin()
def closest_bikes_route():
    args = list(request.args.keys())
    if "latitude" in args and "longitude" in args:  # Check if co-ordinates specified
        try:
            coords = (float(request.args["latitude"]), float(request.args["longitude"]))
            return jsonify(
                get_bike_distances(coords)
            )  # update bike list with distances
        except:
            return jsonify({"error": "Unknown location entered"})
    if (
        "postcode" in args
    ):  # Check if postcode specified (co-ordinates take priority over postcode due to better accuracy)
        try:
            postcode_regex = re.compile(
                r"^([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})$"
            )  # UK government postcode matcher
            if postcode_regex.match(request.args["postcode"]):
                coords = get_coordinates(
                    f"{request.args['postcode']}, United Kingdom"
                )  # make sure its in the UK
                return jsonify(get_bike_distances(coords))
            else:
                return jsonify({"error": "Invalid postcode entered"})
        except:
            return jsonify({"error": "Unknown location entered"})
    else:
        return jsonify({"error": "Either coordinates or postcode required in query"})


def get_bike_distances(coords):
    # update bike list with relative distances
    bike_list = bikes()
    for i, bike in enumerate(bike_list):
        bike_coords = (
            bike["coordinates"]["latitude"],
            bike["coordinates"]["longitude"],
        )
        bike_list[i]["distance"] = get_distance_between(coords, bike_coords)
    bike_list.sort(key=lambda x: x["distance"]["km"])  # sort by distance
    return bike_list


if __name__ == "__main__":
    app.run(debug=True)
