import scrape_mars
from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo


app = Flask(__name__)

# Use PyMongo to establish Mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Render the index.html page.
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mission_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mission_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Insert the record
    mongo.db.collection.update({}, {"$set": mars_data}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)