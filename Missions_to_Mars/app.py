from scrape_mars import *
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
app = Flask(__name__)

app = Flask(__name__)

# # Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission_scraping"
mongo = PyMongo(app)

# identify the collection
mars_data = mongo.db.mars_data
# mars_data.drop()

# Render the index.html page with any craigslist listings in our database.
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    mars_info = mars_data.find_one()

    return render_template("index.html", data_db=mars_info)



# Route that will trigger the scrape function
@app.route("/scrape")
def scraper():

    # Run the scrape function
    mars_data.drop()

    # Insert the record
    scraped_data = scrape()
    mars_data.insert_many([scraped_data])

    # Redirect back to home page
    return redirect("/")
