from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

app = Flask(__name__)

Types = ["Laptops", "Desktop", "Accesories"]

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


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


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("failure.html", message = "Fill it properly")

            
        session["name"] = request.form.get("username")
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods =["POST", "GET"])
def signup():
    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")
        if not username or not password:
            return render_template("faliure.html", message = "Write password and username")
        #user = db.execute("select username from users where username = ?", username)
        #if username == user:
        #   return render_template("faliure.html", message = "you have account already.")
        ##db.execute("INSERT INTO USERS (username, password) VALUES (?, ?)", username, password)
        session['name'] = username
        return redirect("/")
    return render_template("signup.html")


@app.route("/personal")
def personal():
    return render_template("personal.html", types =Types )


@app.route("/logout")
def logout():
    return redirect("/signup")


