from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Homepage of Simulation Api</h1>"


@app.route("/simulation", methods=['POST'])
def run_simulation():
    return request.get_json()


app.run(debug=True)