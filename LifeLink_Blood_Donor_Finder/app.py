from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("lifelink.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS donors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                city TEXT NOT NULL,
                phone TEXT NOT NULL,
                last_donation TEXT,
                available INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                city TEXT NOT NULL,
                units INTEGER NOT NULL,
                hospital TEXT,
                contact TEXT NOT NULL,
                urgency TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/")
def home():
    with get_db() as db:
        donor_count = db.execute("SELECT COUNT(*) FROM donors WHERE available=1").fetchone()[0]
        request_count = db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
        recent_donors = db.execute(
            "SELECT name, blood_group, city FROM donors WHERE available=1 ORDER BY id DESC LIMIT 4"
        ).fetchall()
    return render_template("index.html", donor_count=donor_count,
                           request_count=request_count, recent_donors=recent_donors)

@app.route("/donors")
def donors():
    blood_group = request.args.get("blood_group", "").strip()
    city = request.args.get("city", "").strip()
    query = "SELECT * FROM donors WHERE available=1"
    params = []
    if blood_group:
        query += " AND blood_group=?"
        params.append(blood_group)
    if city:
        query += " AND city LIKE ?"
        params.append(f"%{city}%")
    query += " ORDER BY city, name"
    with get_db() as db:
        results = db.execute(query, params).fetchall()
    return render_template("donors.html", donors=results, blood_group=blood_group, city=city)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = [request.form.get(k, "").strip() for k in
                ("name", "blood_group", "city", "phone", "last_donation")]
        if not all(data[:4]):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("register"))
        with get_db() as db:
            db.execute(
                "INSERT INTO donors (name,blood_group,city,phone,last_donation) VALUES (?,?,?,?,?)",
                data
            )
        flash("Thank you! Your donor profile has been added.", "success")
        return redirect(url_for("donors"))
    return render_template("register.html")

@app.route("/request-blood", methods=["GET", "POST"])
def request_blood():
    if request.method == "POST":
        fields = ("patient_name", "blood_group", "city", "units", "hospital",
                  "contact", "urgency", "details")
        data = [request.form.get(k, "").strip() for k in fields]
        if not all(data[i] for i in (0, 1, 2, 3, 5, 6)):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("request_blood"))
        try:
            units = max(1, min(10, int(data[3])))
        except ValueError:
            flash("Enter a valid number of units.", "error")
            return redirect(url_for("request_blood"))
        with get_db() as db:
            db.execute("""
                INSERT INTO requests
                (patient_name,blood_group,city,units,hospital,contact,urgency,details)
                VALUES (?,?,?,?,?,?,?,?)
            """, [data[0], data[1], data[2], units, data[4], data[5], data[6], data[7]])
        flash("Your request has been saved. Please also contact local hospitals/blood banks for urgent needs.", "success")
        return redirect(url_for("home"))
    return render_template("request.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
