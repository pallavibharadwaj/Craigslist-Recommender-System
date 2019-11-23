from flask import Flask, render_template, jsonify, url_for
from flask_cors import CORS

import charts

app = Flask(__name__)
CORS(app)


@app.route("/")
def recommendation():
    return render_template("recommendation.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/data", methods=['GET'])
def data():
    obj = charts.ChartData()
    value1 = obj.data1()
    value2 = obj.data2()
    value = {
        'val1': value1,
        'val2': value2
    }
    #value = sample()
    return jsonify(value)


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0' , port=5000)
