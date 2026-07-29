from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "dental_secret_key"


# ==========================
# HOME
# ==========================
@app.route("/")
def home():
    conn = get_db_connection()
    doctors = conn.execute("SELECT * FROM doctors").fetchall()
    conn.close()
    return render_template("index.html", doctors=doctors)


# ==========================
# PATIENT REGISTER
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        conn = get_db_connection()

        existing = conn.execute(
            "SELECT * FROM patients WHERE email=?",
            (email,)
        ).fetchone()

        if existing:
            flash("Email already registered!", "danger")
            conn.close()
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn.execute("""
            INSERT INTO patients(name,email,phone,password)
            VALUES(?,?,?,?)
        """,
        (name, email, phone, hashed_password))

        conn.commit()
        conn.close()

        flash("Registration Successful", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================
# PATIENT LOGIN
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        patient = conn.execute(
            "SELECT * FROM patients WHERE email=?",
            (email,)
        ).fetchone()

        conn.close()

        if patient and check_password_hash(patient["password"], password):

            session["patient_id"] = patient["id"]
            session["patient_name"] = patient["name"]

            flash("Login Successful", "success")

            return redirect(url_for("dashboard"))

        flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# ==========================
# LOGOUT
# ==========================
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Successfully", "success")
    return redirect(url_for("home"))


# ==========================
# DASHBOARD
# ==========================
@app.route("/dashboard")
def dashboard():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    patient = conn.execute(
        "SELECT * FROM patients WHERE id=?",
        (session["patient_id"],)
    ).fetchone()

    appointments = conn.execute("""
        SELECT appointments.*, doctors.name AS doctor_name
        FROM appointments
        JOIN doctors
        ON appointments.doctor_id=doctors.id
        WHERE patient_id=?
        ORDER BY appointment_date
    """,
    (session["patient_id"],)).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        patient=patient,
        appointments=appointments
    )


# ==========================
# PROFILE
# ==========================
@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]

        conn.execute("""
            UPDATE patients
            SET name=?, phone=?
            WHERE id=?
        """,
        (name, phone, session["patient_id"]))

        conn.commit()

        flash("Profile Updated Successfully", "success")

    patient = conn.execute(
        "SELECT * FROM patients WHERE id=?",
        (session["patient_id"],)
    ).fetchone()

    conn.close()

    return render_template("profile.html", patient=patient)


# ==========================
# DOCTORS
# ==========================
@app.route("/doctors")
def doctors():

    conn = get_db_connection()

    doctors = conn.execute("""
        SELECT * FROM doctors
    """).fetchall()

    conn.close()

    return render_template("doctors.html", doctors=doctors)


# ==========================
# BOOK APPOINTMENT
# ==========================
@app.route("/booking/<int:doctor_id>", methods=["GET", "POST"])
def booking(doctor_id):

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    doctor = conn.execute(
        "SELECT * FROM doctors WHERE id=?",
        (doctor_id,)
    ).fetchone()

    if request.method == "POST":

        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        reason = request.form["reason"]

        conn.execute("""
            INSERT INTO appointments
            (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            reason,
            status
            )
            VALUES(?,?,?,?,?,?)
        """,
        (
            session["patient_id"],
            doctor_id,
            appointment_date,
            appointment_time,
            reason,
            "Pending"
        ))

        conn.commit()

        conn.close()

        flash("Appointment Booked Successfully", "success")

        return redirect(url_for("appointments"))

    conn.close()

    return render_template(
        "booking.html",
        doctor=doctor
    )


# ==========================
# APPOINTMENTS
# ==========================
@app.route("/appointments")
def appointments():

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    appointments = conn.execute("""
        SELECT
        appointments.*,
        doctors.name AS doctor_name,
        doctors.specialization
        FROM appointments
        JOIN doctors
        ON appointments.doctor_id=doctors.id
        WHERE patient_id=?
        ORDER BY appointment_date DESC
    """,
    (session["patient_id"],)).fetchall()

    conn.close()

    return render_template(
        "appointments.html",
        appointments=appointments
    )


# ==========================
# CANCEL APPOINTMENT
# ==========================
@app.route("/cancel/<int:id>")
def cancel(id):

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("""
        UPDATE appointments
        SET status='Cancelled'
        WHERE id=?
    """,
    (id,))

    conn.commit()

    conn.close()

    flash("Appointment Cancelled", "success")

    return redirect(url_for("appointments"))


# ==========================
# RESCHEDULE
# ==========================
@app.route("/reschedule/<int:id>", methods=["GET", "POST"])
def reschedule(id):

    if "patient_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    appointment = conn.execute(
        "SELECT * FROM appointments WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        date = request.form["appointment_date"]
        time = request.form["appointment_time"]

        conn.execute("""
            UPDATE appointments
            SET appointment_date=?,
                appointment_time=?,
                status='Pending'
            WHERE id=?
        """,
        (date, time, id))

        conn.commit()

        conn.close()

        flash("Appointment Rescheduled", "success")

        return redirect(url_for("appointments"))

    conn.close()

    return render_template(
        "reschedule.html",
        appointment=appointment
    )


# ==========================
# ADMIN LOGIN
# ==========================
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        admin = conn.execute(
            "SELECT * FROM admins WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        if admin and check_password_hash(admin["password"], password):

            session["admin"] = admin["username"]

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Credentials", "danger")

    return render_template("admin_login.html")


# ==========================
# ADMIN DASHBOARD
# ==========================
@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    patient_count = conn.execute(
        "SELECT COUNT(*) FROM patients"
    ).fetchone()[0]

    doctor_count = conn.execute(
        "SELECT COUNT(*) FROM doctors"
    ).fetchone()[0]

    appointment_count = conn.execute(
        "SELECT COUNT(*) FROM appointments"
    ).fetchone()[0]

    doctors = conn.execute("""
        SELECT *
        FROM doctors
        ORDER BY id DESC
    """).fetchall()

    appointments = conn.execute("""
        SELECT
            appointments.*,
            patients.name AS patient_name,
            doctors.name AS doctor_name
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.id
        JOIN doctors
            ON appointments.doctor_id = doctors.id
        ORDER BY appointments.appointment_date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        patient_count=patient_count,
        doctor_count=doctor_count,
        appointment_count=appointment_count,
        doctors=doctors,
        appointments=appointments
    )

# ==========================
# APPROVE APPOINTMENT
# ==========================
@app.route("/admin/approve/<int:id>")
def approve_appointment(id):

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    conn.execute(
        "UPDATE appointments SET status=? WHERE id=?",
        ("Approved", id)
    )

    conn.commit()
    conn.close()

    flash("Appointment Approved Successfully", "success")

    return redirect(url_for("admin_dashboard"))


# ==========================
# REJECT APPOINTMENT
# ==========================
@app.route("/admin/reject/<int:id>")
def reject_appointment(id):

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    conn.execute(
        "UPDATE appointments SET status=? WHERE id=?",
        ("Rejected", id)
    )

    conn.commit()
    conn.close()

    flash("Appointment Rejected Successfully", "warning")

    return redirect(url_for("admin_dashboard"))


# ==========================
# ADD DOCTOR
# ==========================
@app.route("/admin/add-doctor", methods=["GET", "POST"])
def add_doctor():

    if "admin" not in session:
        return redirect(url_for("admin"))

    if request.method == "POST":

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO doctors
            (
                name,
                specialization,
                experience,
                fees,
                image,
                about
            )
            VALUES (?,?,?,?,?,?)
        """, (
            request.form["name"],
            request.form["specialization"],
            request.form["experience"],
            request.form["fees"],
            request.form["image"],
            request.form["about"]
        ))

        conn.commit()
        conn.close()

        flash("Doctor Added Successfully", "success")

        return redirect(url_for("admin_dashboard"))

    return render_template("add_doctor.html")


# ==========================
# EDIT DOCTOR
# ==========================
@app.route("/admin/edit-doctor/<int:id>", methods=["GET", "POST"])
def edit_doctor(id):

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    doctor = conn.execute(
        "SELECT * FROM doctors WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        conn.execute("""
            UPDATE doctors
            SET
                name=?,
                specialization=?,
                experience=?,
                fees=?,
                image=?,
                about=?
            WHERE id=?
        """, (
            request.form["name"],
            request.form["specialization"],
            request.form["experience"],
            request.form["fees"],
            request.form["image"],
            request.form["about"],
            id
        ))

        conn.commit()
        conn.close()

        flash("Doctor Updated Successfully", "success")

        return redirect(url_for("admin_dashboard"))

    conn.close()

    return render_template(
        "edit_doctor.html",
        doctor=doctor
    )


# ==========================
# DELETE DOCTOR
# ==========================
@app.route("/admin/delete-doctor/<int:id>")
def delete_doctor(id):

    if "admin" not in session:
        return redirect(url_for("admin"))

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM doctors WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Doctor Deleted Successfully", "success")

    return redirect(url_for("admin_dashboard"))

# ==========================
# ADMIN LOGOUT
# ==========================
@app.route("/admin/logout")
def admin_logout():

    session.pop("admin", None)

    return redirect(url_for("admin"))


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(debug=True)