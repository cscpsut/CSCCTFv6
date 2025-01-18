from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
import psycopg2
import psycopg2.extras
import random
import string
import secrets
import os
from functools import reduce

random.seed(os.urandom(32))
ADMIN_PASSWORD = ''.join(secrets.choice(string.ascii_uppercase) for _ in range(12))
ADMIN_USERNAME = f"admin-{str(random.random())[2:]}"
ADMIN_SALT = str(random.getrandbits(32))
FLAG = os.getenv("FLAG", "flag{this_is_a_fake_flag}")

print(f"Admin username: {ADMIN_USERNAME}")
print(f"Admin password: {ADMIN_PASSWORD}")

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "GrVjmF$&S?dS%3Q'%rY\\/-\n_<Co\r]iIK"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD"),
        host = "localhost",
    )
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            user_info TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            seed BIGINT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    cursor.execute(
        'INSERT INTO users (username, password, salt, user_info) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
        (ADMIN_USERNAME, hash_password(ADMIN_PASSWORD, ADMIN_SALT), ADMIN_SALT, FLAG)
    )
    conn.commit()
    conn.close()

def hash_password(a: str, b: str) -> str:
    return ''.join(
        (lambda x: (
            hex(reduce(
                lambda r, _: r ^ ord(x[1]) ^ ord(x[1]),
                range(sum([7] * 143)),
                ord(x[0])
            ) ^ ord(x[1]))[2:].zfill(2)
        ))((c1, c2))
        for c1, c2 in zip(
            a + '\0' * ((len(b) - len(a)) * (len(b) > len(a))),
            b + '\0' * ((len(a) - len(b)) * (len(a) > len(b)))
        )
    )

def authenticate_user(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT id, password, salt FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    if len(hash_password(password, user["salt"])) != len(user["password"]):
        return None

    for i in range(len(hash_password(password, user["salt"]))):
        if hash_password(password, user["salt"])[i] != user['password'][i]:
            return False

    return user["id"]

def generate_minesweeper_grid(seed: int):
    random.seed(seed)
    size = 10
    mines = 15
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for _ in range(mines):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        while grid[x][y] == -1:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        grid[x][y] = -1
    return grid

def get_seed_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    seed = random.getrandbits(32)
    cursor.execute("INSERT INTO games (user_id, seed) VALUES (%s, %s)", (user_id, seed))
    conn.commit()
    conn.close()
    return seed

create_tables()

@app.route("/debug")
def debug():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify([dict(user) for user in users])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_info = request.form["user_info"]

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            salt = str(random.getrandbits(32))
            hashed_password = hash_password(password, salt)
            cursor.execute("INSERT INTO users (username, password, salt, user_info) VALUES (%s, %s, %s, %s)",
                            (username, hashed_password, salt, user_info))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            flash("Username already exists", "error")
            return redirect(url_for("signup"))
        conn.close()
        flash("Signup successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = authenticate_user(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please log in to access the profile.", "error")
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT username, password, user_info FROM users WHERE id = %s", (session["user_id"],))
    user = cursor.fetchone()
    conn.close()
    return render_template("profile.html", user=user)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT seed, timestamp FROM games WHERE user_id = %s ORDER BY timestamp DESC LIMIT 10", (session["user_id"],))
    games = cursor.fetchall()
    print(games)
    cursor.execute("SELECT username, score FROM leaderboard ORDER BY score DESC LIMIT 10")
    leaderboard = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", 
                            username=session.get("username"),
                            games=games,
                            leaderboard=leaderboard)

@app.route("/start-game", methods=["POST"])
def start_game():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 403

    seed = get_seed_for_user(session["user_id"])
    grid = generate_minesweeper_grid(seed)
    return jsonify(grid)


@app.route("/update-score", methods=["POST"])
def update_score():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor()

    score = 100

    try:
        cursor.execute(
            "SELECT id, score FROM leaderboard WHERE username = %s",
            (session["username"],)
        )
        existing_score = cursor.fetchone()
        
        if existing_score:
            if score > existing_score[1]:
                cursor.execute(
                    "UPDATE leaderboard SET score = %s WHERE username = %s",
                    (score, session["username"])
                )
        else:
            cursor.execute(
                "INSERT INTO leaderboard (username, score) VALUES (%s, %s)",
                (session["username"], score)
            )
        
        conn.commit()
        return jsonify({"success": True, "score": score})

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)