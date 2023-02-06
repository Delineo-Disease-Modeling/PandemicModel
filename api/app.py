from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequest
import delineo as sim

app = Flask(__name__)

# CORS
cors = CORS(app)


@app.route("/simulation/", methods=["POST", "GET"])
@cross_origin()
def run_simulation():
    try:
        request.get_json(force=True)
    except BadRequest:
        return "Bad Request"
    if request.json:
        error_missing_data = "Missing Required Data"
        error_invalid_data = "Invalid Data"

        try:
            check1 = request.json["maskPercent"]
            if not isinstance(check1, int):
                return error_invalid_data

            check2 = request.json["capacityPercent"]
            if not isinstance(check2, int):
                return error_invalid_data

            check3 = request.json["massPercent"]
            if not isinstance(check3, int):
                return error_invalid_data

            check4 = request.json["schoolsShutdown"]
            if not isinstance(check4, int):
                return error_invalid_data

            check5 = request.json["stayAtHome"]
            if not isinstance(check5, (bool, int)):
                return error_invalid_data

            check6 = request.json["vaccinePercent"]
            if not isinstance(check6, int):
                return error_invalid_data

            check7 = request.json["location"]
            if not isinstance(check7, str):
                return error_invalid_data

            check8 = request.json["useDB"]
            if not isinstance(check8, (bool, int)):
                return error_invalid_data

        except KeyError:
            return error_missing_data

        interventions = {
            "maskWearing": check1,
            "roomCapacity": check2,
            "dailyTesting": check3,
            "contactTracing": check4,
            "stayAtHome": check5,
            "vaccinatedPercent": check6,
        }
        return sim.runSimulation(check7, False, 61, interventions, check8)
    else:
        return "Nothing Sent"


@app.route("/", methods=["POST", "GET"])
@cross_origin()
def covidmod_responder():
    try:
        request.get_json(force=True)
    except BadRequest:
        return "Bad Request"
    if request.json:
        error_missing_data = "Missing Required Data"
        error_invalid_data = "Invalid Data"

        try:
            check1 = request.json["maskWearing"]
            if not isinstance(check1, int):
                return error_invalid_data

            check2 = request.json["roomCapacity"]
            if not isinstance(check2, int):
                return error_invalid_data

            check3 = request.json["dailyTesting"]
            if not isinstance(check3, int):
                return error_invalid_data

            check4 = request.json["contactTracing"]
            if not isinstance(check4, int):
                return error_invalid_data

            check5 = request.json["stayHome"]
            if not isinstance(check5, (bool, int)):
                return error_invalid_data

            check6 = request.json["vaccinatedPercent"]
            if not isinstance(check6, int):
                return error_invalid_data

        except KeyError:
            return error_missing_data

        interventions = {
            "maskWearing": check1,
            "roomCapacity": check2,
            "dailyTesting": check3,
            "contactTracing": check4,
            "stayAtHome": check5,
            "vaccinatedPercent": check6,
        }
        return sim.runSimulation("AnyTown", False, 61, interventions, True)
    else:
        return "Nothing Sent"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
