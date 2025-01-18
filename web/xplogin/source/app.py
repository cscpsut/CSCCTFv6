from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import secrets
import random
import time
import os

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)


def execute_db(statement, params=()):
    try:
        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute(statement, params)
            result = c.fetchall()
            conn.commit()
        return result
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", action="register")

    data = request.form
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return render_template(
            "register.html", action="register", error="Username or password is empty!"
        )

    user = execute_db("SELECT * FROM users WHERE username=?", (username,))
    if user:
        return render_template(
            "register.html", action="register", error="User already exists!"
        )
    else:
        execute_db(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html", action="login")

    client_ip = request.remote_addr

    data = request.form
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return render_template(
            "login.html", action="login", error="Username or password is empty!"
        )

    user = execute_db(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password)
    )
    if user:
        execute_db("DELETE FROM ratelimit WHERE ip_address=?", (client_ip,))
        session["username"] = username
        session["logged_in"] = True
        return redirect(url_for("home"))
    else:
        return render_template("login.html", action="login", error="Login failed!")


@app.route("/forgot_password", methods=["POST", "GET"])
def forgot_password():
    if request.method == "GET":
        return render_template("forget.html", action="forgot_password")

    data = request.form
    username = data.get("username")
    if not username:
        return render_template(
            "forget.html", action="forgot_password", error="Username is empty!"
        )

    user = execute_db("SELECT * FROM users WHERE username=?", (username,))
    if user:
        otp = random.randint(1000, 10000)
        print(otp)
        execute_db("UPDATE users SET OTP=? WHERE username=?", (otp, username))
        # Here you would send an email with the OTP
        return redirect(url_for("reset_password"))
    else:
        return render_template(
            "forget.html", action="forgot_password", error="User not found!"
        )


@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if request.method == "GET":
        return render_template("reset.html", action="reset_password")

    client_ip = request.remote_addr
    data = request.form
    username = data.get("username")
    new_password = data.get("new_password")
    otp = data.get("otp")

    if not username or not new_password or not otp:
        return render_template(
            "reset.html", action="reset_password", error="All fields are required!"
        )
    user = execute_db("SELECT * FROM users WHERE username=?", (username,))
    if user:
        rate_limit = execute_db(
            "SELECT * FROM ratelimit WHERE ip_address=?", (client_ip,)
        )
        current_time = time.time()

        # Check if it is the first attempt

        if rate_limit:  # if rate limit is 1 or more
            attempts = rate_limit[0][1]

            # Check if the user has exceeded the maximum number of attempts
            if attempts >= 5:
                return render_template(
                    "reset.html",
                    action="reset_password",
                    error="Too many incorrect OTP attempts. Please try again later.",
                )
            # Check if otp is correct
            if str(user[0][2]) == otp:
                execute_db(
                    "UPDATE users SET password=?, OTP=NULL WHERE username=?",
                    (new_password, username),
                )
                execute_db("DELETE FROM ratelimit WHERE ip_address=?", (client_ip,))
                return redirect(url_for("login"))
            else:
                # if otp is incorrect increment the number of failed attempts
                execute_db(
                    "UPDATE ratelimit SET attempts=?, last_attempt_time=? WHERE ip_address=?",
                    (attempts + 1, current_time, client_ip),
                )
                return render_template(
                    "reset.html", action="reset_password", error="OTP is invalid!"
                )
        else:  # if rate limit is 0
            # Check if otp is correct
            if user[0][2] == otp:
                execute_db(
                    "UPDATE users SET password=?, OTP=NULL WHERE username=?",
                    (new_password, username),
                )
                return redirect(url_for("login"))
            else:  # if otp is incorrect insert the ip address into the rate limit table
                execute_db(
                    "INSERT INTO ratelimit (ip_address, attempts, last_attempt_time) VALUES (?, ?, ?)",
                    (client_ip, 1, current_time),
                )
                return render_template(
                    "reset.html", action="reset_password", error="OTP is invalid!"
                )
    else:  # if user does not exist
        return render_template("reset.html", action="reset_password", error="Error!")


@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if session.get("username") != "admin":
        return render_template("home.html")
    return render_template("home.html", success=True, flag=FLAG)


@app.route("/")
def root():
    return redirect(url_for("home"))


if __name__ == "__main__":
    FLAG = os.getenv("FLAG", "CSCCTF{FAKE_FLAG_FOR_TESTING}")
    # Initialize the database
    execute_db(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY UNIQUE, password TEXT NOT NULL, OTP int)"
    )
    execute_db(
        "CREATE TABLE IF NOT EXISTS ratelimit (ip_address TEXT PRIMARY KEY, attempts INTEGER, last_attempt_time REAL)"
    )
    # Create admin account if it doesn't exist
    user = execute_db("SELECT * FROM users WHERE username=?", ("admin",))
    if not user:
        execute_db(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", secrets.token_hex(16)),
        )
    app.run(debug=False, host="0.0.0.0", port=1337)
