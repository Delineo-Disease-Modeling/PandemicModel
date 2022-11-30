from flask import Flask, request

import Delineo_Simulation as sim
app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Homepage of Simulation Api</h1>"


@app.route("/simulation", methods=['POST'])
def run_simulation():
    mc = sim.MasterController()
    mc.runFacilityTests('facilities_info.txt')
    return request.get_json()


@app.route("/covid_ui", methods=['POST'])
def run_simulation2():
    mc = sim.MasterController()
    mc.runFacilityTests('facilities_info.txt')
    return request.get_json()


app.run(host="", debug=True, port=5000, threaded=True)
