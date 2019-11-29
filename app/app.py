from flask import Flask, render_template, jsonify, url_for, request
from flask_cors import CORS

import charts, home

app = Flask(__name__)
CORS(app)


@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/favorites")
def favorites():
    return render_template("favorites.html")

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

@app.route("/homedata", methods=['GET'])
def homedata():
    obj = home.ListingData()
    value = obj.getAllListings()
    return jsonify(value)

@app.route("/add_favorite", methods=['GET'])
def add_favorite():
    postingid = request.args.get('postingid')
    obj = home.ListingData()
    value = obj.add_favorite(postingid)
    return jsonify(value)

@app.route("/favoritesdata", methods=['GET'])
def favoritesdata():
    obj = home.ListingData()
    value = obj.getAllListings()
    return jsonify(value)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0' , port=5000)
