from scrape_mars import *
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
app = Flask(__name__)

@app.route("/")
def index():
    data = {"first_name": "Sarah",
    "last_name": "Aray"}
    return render_template("index.html",result = data)

@app.route("/scrape")
def scrape_mars():
    return scrape()

if __name__ == "__main__":
    app.run()

