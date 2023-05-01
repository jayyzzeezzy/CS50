import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    # create sql query in python by using db.execute()
    transactions_db = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price, name, SUM(trans_total) AS trans_total FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = cash_db[0]["cash"]

    return render_template("index.html", database=transactions_db, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:
        # get user's iniput for desire symbol
        symbol = request.form.get("symbol")

        # if user did not enter a symbol
        if not symbol:
            return apology("Must Enter a Symbol")

        try:
        # get user's input for number of shares
            shares = int(request.form.get("shares"))

        # handles situations when user put in fractions and words
        except ValueError:
            return apology("Must Enter a Whole Number")

        # use the lookup() function that was already written in help.py
        stock = lookup(symbol.upper())

        # if user entered a symbol that does not exist
        if stock == None:
            return apology("Symbol Does Not Exist")

        # user entered negative shares
        if shares < 0:
            return apology("Must Enter a Positive Number")

        # how much is this purchase worth
        transaction_value = shares * stock["price"]

        user_id = session["user_id"]

        # find out how much cash the user have at the time of purchase
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        # render apology() if the user doesn't have enough money in the account at the time of purchase
        if user_cash < transaction_value:
            return apology("Not Enough Funds")

        # update the amount of cash user has left after making one transaction
        update_cash = user_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        # get the most current time at the time of making transaction
        date = datetime.datetime.now()

        # insert user's purchase info into the transactions table
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, name, trans_total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], shares, stock["price"], date, stock["name"], transaction_value)

        flash("Purchase!")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    # use db.execute() to access the transactions table
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions_db)

# my personal touch, allow user to deposit more funds into their account


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Allow user to deposit more funds"""
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("deposit.html")
    else:
        # get user's input on how much they want to deposit
        deposit = int(request.form.get("deposit"))

        if not deposit:
            return apology("You Must Enter an Amount")

        # find out how much cash this user have at the point of deposit
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        # update the amount of cash user has after making the deposit
        update_cash = user_cash + deposit
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        return redirect("/")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        # if user did not enter a symbol
        if not symbol:
            return apology("Must Enter a Symbol")

        # use the lookup() function that was already written in help.py
        stock = lookup(symbol.upper())

        # if user entered a symbol that does not exist
        if stock == None:
            return apology("Symbol Does Not Exist")

        # if a symbol exists then return the following info
        return render_template("quoted.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

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

        # Make a variable to hash password
        hash = generate_password_hash(password)

        # Code below is taken referrence from youtube
        # if try goes thru then username has not exist before
        # if except goes thru then this username has already exists
        try:
            # From W3School: INSERT INTO table_name (column1, column2, column3, ...) VALUES (value1, value2, value3, ...);
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")

        # implement session to mark this user's login info
        # taken from the login route
        session["user_id"] = new_user

        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbol_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbol_user])

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # if user did not enter a symbol
        if not symbol:
            return apology("Must Enter a Symbol")

        # use the lookup() function that was already written in help.py
        stock = lookup(symbol.upper())

        # if user entered a symbol that does not exist
        if stock == None:
            return apology("Symbol Does Not Exist")

        if shares < 0:
            return apology("Must Enter a Positive Number")

        # checks how much is this sale worth
        # quantiy times price of stock
        transaction_value = shares * stock["price"]

        user_id = session["user_id"]

        # find out how much cash the user have at the time of sale
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        # find out how many shares the user has at the time of sale
        user_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = ? AND symbol = ?", user_id, symbol)
        user_shares_real = user_shares[0]["shares"]

        if shares > user_shares_real:
            return apology("You Do Not Own This Many Shares")

        # update the amount of cash user has left after making one transaction
        update_cash = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)

        # get the most current time at the time of making transaction
        date = datetime.datetime.now()

        # this line handles negative shares and trans_total
        # when you make a sale, you lose shares and total of the stock value (trans_total is the name I use for now)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date, name, trans_total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1)*shares, stock["price"], date, stock["name"], (-1)*transaction_value)

        flash("Sold!")

        return redirect("/")
