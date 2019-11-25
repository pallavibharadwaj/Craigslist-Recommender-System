from flask import Flask, render_template, jsonify, url_for
from flask_cors import CORS

import charts, recommender

app = Flask(__name__)
CORS(app)


@app.route("/")
def recommendation():
    return render_template("recommendation.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/chartdata", methods=['GET'])
def chartdata():
    obj = charts.ChartData()
    value1 = obj.data1()
    value2 = obj.data2()
    value = {
        'val1': value1,
        'val2': value2
    }
    return jsonify(value)

@app.route("/postdata", methods=['GET'])
def postdata():
    obj = recommender.ListingData()
    value = obj.getAllListings()
    return jsonify(value)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0' , port=5000)
