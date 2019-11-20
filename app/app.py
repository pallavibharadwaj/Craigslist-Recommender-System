from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def recommendation():
    return render_template("recommendation.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")
    
if __name__ == "__main__":
    app.run(debug=True)
