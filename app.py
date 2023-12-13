from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

app = Flask(__name__)

Types = ["Laptops", "Desktop", "Accesories"]

@app.route("/")
@app.route("/Home")
def home():
    return render_template("index.html", types =Types )
