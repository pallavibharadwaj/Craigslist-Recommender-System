from flask import Flask, render_template, jsonify, url_for, request
from flask_cors import CORS

import charts, home, recommender

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
    posts = obj.getpostcount()
    medianrent = obj.median_rent()
    petanimals = obj.pet_animals()
    wheelchair = obj.wheelchair()
    average_price = obj.getaverageprice()
    boxplot = obj.getboxplotvalues()
    spline = obj.getsplinevalues()
    value = {
        'heatmap_posts': posts,
        'medianrent':medianrent,
        'petanimals':petanimals,
        'wheelchair':wheelchair,
        'heatmap_price': average_price,
        'boxplot' : boxplot,
        'spline' : spline
    }
    return jsonify(value)

@app.route("/homedata", methods=['GET'])
def homedata():
    city = request.args.get('city')
    beds = request.args.get('beds')
    postingid = request.args.get('postingid')
    obj = home.ListingData()
    value = obj.getAllListings(city, beds, postingid)
    return jsonify(value)

@app.route("/add_favorite", methods=['GET'])
def add_favorite():
    postingid = request.args.get('postingid')
    obj = home.ListingData()
    value = obj.add_favorite(postingid)
    return jsonify(value)

@app.route("/favoritesdata", methods=['GET'])
def favoritesdata():
    obj = recommender.ListingData()
    favorites = obj.getAllFavorites()
    similar = obj.getAllSimilar()
    value = {
        'favorites': favorites,
        'similar': similar
    }
    return jsonify(value)

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0' , port=5000)
