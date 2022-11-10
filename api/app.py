from flask import Flask, request
from simulation.master import MasterController

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Homepage of Simulation Api</h1>"


@app.route("/simulation", methods=['POST'])
def run_simulation():
    mc = MasterController()
    mc.runFacilityTests('facilities_info.txt')
    return request.get_json()


app.run(debug=True)