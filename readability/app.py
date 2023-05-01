import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# list of available statuses for work orders (hard coded for anti hack purpose)
STATUSES = [
    "Pending",
    "Dispatched worker",
    "Completed"
]

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show status on work orders"""
    user_id = session["user_id"]

    # role_db = db.execute("SELECT role FROM users WHERE id = ?", user_id)

    # unfinished work orders are on top
    status_db = db.execute("SELECT id, apt, date, time, status FROM workorder WHERE user_id = ? AND status != 'Completed'", user_id)
    # ORDER BY status IS 'Completed'", user_id)

    completedb = db.execute("SELECT id, apt, date, time, status FROM workorder WHERE user_id = ? AND status == 'Completed'", user_id)
    return render_template("index.html", database=status_db, completes=completedb)


@app.route("/maintenance", methods=["GET", "POST"])
@login_required
def maintenance():
    """Put in a work order for maintenance"""
    # user reached route via GET
    if request.method == "GET":
        return render_template("maintenance.html")
    # user reached route via POST (by submitting a form via POST)
    else:
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        apt = request.form.get("apt")
        description = request.form.get("description")
        permission = request.form.get("permission")
        pet = request.form.get("pet")
        date = request.form.get("date")
        time = request.form.get("time")
        note = request.form.get("note")

        # If user did not enter a first name, last name, email, phone,
        # apt, description, permission, pet, date, time, note
        if not fname:
            return apology("Must Enter a First Name")
        if not lname:
            return apology("Must Enter a Last Name")
        if not email:
            return apology("Must Enter an Email")
        if not phone:
            return apology("Must Enter a Phone Number")
        if not apt:
            return apology("Must Enter an APT Number")
        if not description:
            return apology("Must Enter a Brief Description")
        if not permission:
            return apology("Must Select in the Permission Section")
        if not pet:
            return apology("Must Select in the Pet Section")
        if not date:
            return apology("Must Provide a Date")
        if not time:
            return apology("Must Provide a Time")

        user_id = session["user_id"]

        # insert form into the workorder table
        db.execute("INSERT INTO workorder (fname, lname, email, phone, apt, description, permission, pet, date, time, note, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   fname, lname, email, phone, apt, description, permission, pet, date, time, note, user_id)

        flash("Submitted!")

        return redirect("/")


@app.route("/status", methods=["GET", "POST"])
@login_required
def status():
    """Allow users to update the status on work orders"""
    # user reached route via GET (as by clicking a link or by redirect)
    if request.method == "GET":
        user_id = session["user_id"]
        workorders = db.execute("SELECT id FROM workorder WHERE user_id = ?", user_id)
        return render_template("status.html", statuses=STATUSES, status_ids=[row["id"] for row in workorders])

    # if request.method == "GET":
    #     return render_template("status.html")
    # user reached route via POST (by submitting a form via POST)
    else:
        # user_id = session["user_id"]
        status_id = request.form.get("status_id")
        update_status = request.form.get("update_status")

        if not status_id or not update_status:
            return apology("Please Select All Fields")
        db.execute("UPDATE workorder SET status = ? WHERE id = ?", update_status, status_id)

        # update_db = db.execute("SELECT id, apt, date, time, status FROM workorder WHERE user_id = ? ORDER BY status", user_id)

        flash("Status updated!")

        return redirect("/")


# sampled from youtube
@app.route("/inbox")
@login_required
def inbox():
    """Allow user to send maintenance messages"""
    user_id = session["user_id"]
    username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_db[0]["username"]
    messages = db.execute("SELECT * FROM messages WHERE recipient = ?", username)
    return render_template("/inbox.html", messages=messages)


# sampled from youtube
@app.route("/message", methods=["GET", "POST"])
@login_required
def message():
    """Allow user to compose a message"""
    # if request.method == "GET":
    #     user_id = session["user_id"]
    #     workorders = db.execute("SELECT id FROM workorder WHERE user_id = ?", user_id)
    #     return render_template("status.html", workorderIDs=[row["id"] for row in workorders])
    if request.method == "GET":
        return render_template("message.html")

    else:
        workorder_id = request.form.get("workorder_id")
        apt = request.form.get("apt")
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not workorder_id or not apt or not sender or not recipient or not subject or not body:
            return apology("Please Do Not Leave Empty Fields")

        db.execute("INSERT INTO messages (workorder_id, apt, sender, recipient, subject, body) VALUES (?, ?, ?, ?, ?, ?)", workorder_id, apt, sender, recipient, subject, body)

        flash("Sent!")

        return redirect("/sent")


# how user all outgoing messages
# display sender as the user, and recipient as whoever they sent message to
@app.route("/sent")
@login_required
def sent():
    """Show sent emails"""
    user_id = session["user_id"]
    username_db = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = username_db[0]["username"]
    messages = db.execute("SELECT * FROM messages WHERE sender = ?", username)
    return render_template("/sent.html", messages=messages)


# show user details about their message
@app.route("/view", methods=["POST"])
@login_required
def view():
    """View message details"""
    if request.method == "POST":
        message_id = request.form.get("message_id")
        message_detailDB = db.execute("SELECT * FROM messages WHERE id = ?", message_id)
        message_detail = message_detailDB[0]
        return render_template("view.html", message_detail=message_detail)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        role = request.form.get("role")

        # If user did not enter a username
        if not username:
            return apology("Must Enter a Username")
        # if user did not enter a password
        if not password:
            return apology("Must Enter a Password")
        # if user did not enter a confirmation
        if not confirmation:
            return apology("Must Enter a Confirmation")

        # if password and confirmation are different
        if password != confirmation:
            return apology("Passwords Do Not Match!")

        # if user did not select tenant or contractor
        if not role:
            return apology("Must Select a Role!")

        # Make a variable to hash password
        hash = generate_password_hash(password)

        # if try goes thru then username has not exist before
        # if except goes thru then this username has already exists
        try:
            # From W3School: INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
            new_user = db.execute(
                "INSERT INTO users (username, hash, role) VALUES (?, ?, ?)", username, hash, role)
        except:
            return apology("Username already exists")

        # implement session to mark this user's login info
        # taken from the login route
        session["user_id"] = new_user

        return redirect("/maintenance")

@app.route("/reply", methods=["POST"])
@login_required
def reply():
    """Reply the message on message detail view"""
    if request.method == "POST":
        message_id = request.form.get("message_id")
        message_detailDB = db.execute("SELECT * FROM messages WHERE id = ?", message_id)
        message_detail = message_detailDB[0]
        return render_template("reply.html", message_detail=message_detail)