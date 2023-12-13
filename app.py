from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)

Types = ["Laptops", "Desktop", "Accesories"]



@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", types =Types )


@app.route("/about")
def about():
    return render_template("about.html", types =Types )


@app.route("/contact")
def contact():
    return render_template("contact.html", types =Types )

@app.route("/fav")
def fav():
    return render_template("fav.html", types =Types )


@app.route("/login")
def login():
    return render_template("login.html", types =Types )


@app.route("/signup")
def signup():
    return render_template("signup.html", types =Types )


@app.route("/personal")
def personal():
    return render_template("personal.html", types =Types )


@app.route("/logout")
def logout():
    return redirect("/signup")


