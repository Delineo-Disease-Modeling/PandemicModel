from flask import Flask, request, json
import delineo as sim
app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Homepage of Simulation Api</h1>"


@app.route("/simulation")
def run_simulation(**kwargs):
    data = sim.runSimulation('Anytown', False, 1, {}, True)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')
    return response


app.run(host="", debug=True, port=5000, threaded=True)


def write_to_file(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()
