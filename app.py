from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "dental_secret_key"


# ===========================
# Home
# ===========================

@app.route("/")
def home():
    conn = get_db_connection()
    doctors = conn.execute("SELECT * FROM doctors").fetchall()
    conn.close()
    return render_template("index.html", doctors=doctors)


# ===========================
# Register
# ===========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        address = request.form["address"]
        password = request.form["password"]

        conn = get_db_connection()

        patient = conn.execute(
            "SELECT * FROM patients WHERE email=?",
            (email,)
        ).fetchone()

        if patient:
            flash("Email already registered.")
            conn.close()
            return redirect(url_for("register"))

        conn.execute("""
        INSERT INTO patients
        (name,age,gender,mobile,email,address,password)
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            name,
            age,
            gender,
            mobile,
            email,
            address,
            password
        ))

        conn.commit()
        conn.close()

        flash("Registration Successful")
        return redirect(url_for("login"))

    return render_template("register.html")


# ===========================
# Login
# ===========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        patient = conn.execute(
            """
            SELECT * FROM patients
            WHERE email=? AND password=?
            """,
            (email, password)
        ).fetchone()

        conn.close()

        if patient:

            session["patient_id"] = patient["id"]
            session["patient_name"] = patient["name"]

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password")

    return render_template("login.html")


# ===========================
# Dashboard
# ===========================

@app.route("/dashboard")
def dashboard():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    appointments = conn.execute("""

    SELECT
    appointments.*,
    doctors.name as doctor_name

    FROM appointments

    JOIN doctors

    ON appointments.doctor_id = doctors.id

    WHERE patient_id=?

    ORDER BY appointment_date

    """, (session["patient_id"],)).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        appointments=appointments
    )


# ===========================
# Logout
# ===========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ===========================
# Doctors
# ===========================

@app.route("/doctors")
def doctors():

    conn = get_db_connection()

    doctors = conn.execute(
        "SELECT * FROM doctors"
    ).fetchall()

    conn.close()

    return render_template(
        "doctor_profile.html",
        doctors=doctors
    )


# ===========================
# Booking
# ===========================

@app.route("/booking", methods=["GET", "POST"])
def booking():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    doctors = conn.execute(
        "SELECT * FROM doctors"
    ).fetchall()

    if request.method == "POST":

        doctor_id = request.form["doctor"]
        treatment = request.form["treatment"]
        date = request.form["date"]
        time = request.form["time"]

        conn.execute("""

        INSERT INTO appointments

        (patient_id,doctor_id,treatment,
        appointment_date,
        appointment_time)

        VALUES(?,?,?,?,?)

        """,

        (
            session["patient_id"],
            doctor_id,
            treatment,
            date,
            time
        ))

        conn.commit()

        conn.close()

        flash("Appointment Booked Successfully")

        return redirect(url_for("dashboard"))

    conn.close()

    return render_template(
        "booking.html",
        doctors=doctors
    )

# ===========================
# Appointment History
# ===========================

@app.route("/appointments")
def appointments():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    appointments = conn.execute("""

    SELECT
    appointments.*,
    doctors.name as doctor_name,
    doctors.specialization

    FROM appointments

    JOIN doctors

    ON appointments.doctor_id=doctors.id

    WHERE patient_id=?

    ORDER BY appointment_date DESC

    """,

    (session["patient_id"],)

    ).fetchall()

    conn.close()

    return render_template(
        "appointments.html",
        appointments=appointments
    )


# ===========================
# Cancel Appointment
# ===========================

@app.route("/cancel/<int:id>")
def cancel(id):

    conn = get_db_connection()

    conn.execute(
        "UPDATE appointments SET status='Cancelled' WHERE id=?",
        (id,)
    )

    conn.commit()

    conn.close()

    flash("Appointment Cancelled")

    return redirect(url_for("appointments"))


# ===========================
# Reschedule
# ===========================

@app.route("/reschedule/<int:id>", methods=["GET", "POST"])
def reschedule(id):

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":

        date = request.form["date"]
        time = request.form["time"]

        conn.execute("""

        UPDATE appointments

        SET
        appointment_date=?,
        appointment_time=?,
        status='Pending'

        WHERE id=?

        """,

        (
            date,
            time,
            id
        ))

        conn.commit()

        conn.close()

        flash("Appointment Rescheduled")

        return redirect(url_for("appointments"))

    appointment = conn.execute(
        "SELECT * FROM appointments WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "reschedule.html",
        appointment=appointment
    )


# ===========================
# Run App
# ===========================

if __name__ == "__main__":
    app.run(debug=True)