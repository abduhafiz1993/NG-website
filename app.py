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
    if not session["user_id"]:
        return redirect("/login")
    rows = db.execute("SELECT * FROM Users WHERE user_id = ?", session["user_id"])
    return render_template("personal.html", types =Types, personal=rows )

@app.route("/update_info", methods=["POST"])
def update_info():
    db.execute(
            "update Users set username = ? , email = ? where user_id = ?",
            request.form.get("username"),
            request.form.get("email"),
            session["user_id"] 
        )
    return redirect("/personal")

@app.route("/add", methods = ["POST", "GET"])
def add():
    if request.method == "POST":
        db.execute(
            "INSERT INTO Users (username, password, email, role) VALUES(?, ?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
            request.form.get("email"),
            request.form.get("role")
        )
        return render_template("add.html")
    return render_template("add.html")
    
@app.route("/feedback", methods = ["POST"])
def feedback():
        db.execute(
            "INSERT INTO Feedbacks (name, email, message) VALUES(?, ?, ?)",
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("message"),
        )
        return redirect("/")
    

@app.route("/")
@app.route("/home")
def home():
    products = db.execute("SELECT * FROM Products ORDER BY created_at DESC LIMIT 16")

    return render_template("index.html", types =Types, products= products)


@app.route("/about")
def about():
    return render_template("about.html", types =Types )

@app.route("/dash")
def dash():
    messages = db.execute("select * from message order by CURRENT_TIMESTAMP desc")
    feedbacks = db.execute("select * from Feedbacks order by CURRENT_TIMESTAMP desc")
    return render_template("dash.html", messages = messages, feedbacks= feedbacks )


@app.route("/contact", methods =['POST', 'GET'])
def contact():
    if request.method == 'POST':
        db.execute(
            "INSERT INTO message (name, email, message) VALUES(?, ?, ?)",
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("message"),
        )
        return render_template("contact.html", types =Types)
    return render_template("contact.html", types =Types )




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
        if rows[0]["role"] != 'Customer':
            return redirect("/admin")
        return redirect("/")
    return render_template("login.html")


@app.route("/admin")
def admin():
    if not session["user_id"]:
        return redirect("/login")
    rows = db.execute("SELECT * FROM Users WHERE user_id = ?", session["user_id"])
    if rows[0]["role"] == 'Customer':
        return redirect("/")
    customer = db.execute("SELECT * FROM Users where role = ?", 'Customer')
    role = rows[0]["role"]
    return render_template("admin.html" , role = role, customer = customer)
    

@app.route("/product", methods =["POST", "GET"])
def product():
    role = 'Customer'
    if session["user_id"]:
        rows = db.execute("SELECT * FROM Users WHERE user_id = ?", session["user_id"])
        role = rows[0]["role"]
    if request.method == 'POST':
        products = db.execute("select * from Products where type_id = (select type_id from Types where type_name = ?) ORDER BY created_at DESC limit 32", request.form.get("id"))
        return render_template("product.html", products = products, role=role)
        
    products = db.execute("select * from Products ORDER BY created_at DESC limit 32")
    return render_template("product.html", products = products, role=role)

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