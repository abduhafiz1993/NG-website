from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

db = SQL("sqlite:///database.db")
Types = db.execute("select * from Types")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.route("/personal")
def personal():
    return render_template("personal.html", types =Types )


@app.route("/")
@app.route("/home")
def home():
    products = db.execute("SELECT * FROM Products ORDER BY created_at DESC ")

    return render_template("index.html", types =Types, products= products)


@app.route("/about")
def about():
    return render_template("about.html", types =Types )


@app.route("/contact")
def contact():
    return render_template("contact.html", types =Types )

@app.route("/rem", methods=["POST"])
def removess():
    id = int(request.form.get("id"))
    if id:
        if "favriote" in session and id in session["favriote"]:
            session["favriote"].remove(id)
        products = db.execute("SELECT * FROM Products where product_id in (?)", session["favriote"])
        return redirect("/fav", products =products)
    return redirect("/fav")




@app.route("/fav", methods=["POST", "GET"])
def fav():
    if not session:
        return redirect("/login")

    if not "favriote" in session:
        session["favriote"] = []
    
    if request.method == "POST":
        id = request.form.get("id")
        if id:
            if not id  in session["favriote"]:
                session["favriote"].append(id)
                return
    elif request.method == "GET":
        if len(session["favriote"]) != 0:
            products = db.execute("SELECT * FROM Products where product_id in (?)", session["favorite"])
        else:
            products = []
        return render_template("fav.html", types =Types, products =products )





@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("faliure.html", message = "username must provided")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("faliure.html", message = "password must provided")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM Users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
                return render_template("faliure.html", message = "invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods =["POST", "GET"])
def signup():
    
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("faliure.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("faliure.html", message="must provide password")
        elif not request.form.get("email"):
            return render_template("faliure.html", message="must provide email")
        rows = db.execute(
            "SELECT * FROM Users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return render_template("faliure.html", message="username already exist")
        db.execute(
            "INSERT INTO Users (username, password, email) VALUES(?, ?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
            request.form.get("email"),
        )
        rows = db.execute(
            "SELECT * FROM Users WHERE username = ?",
            request.form.get("username"),
        )
        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/home")

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")