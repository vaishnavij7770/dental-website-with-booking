import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "dental.db"


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # ==========================
    # Patients Table
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ==========================
    # Doctors Table
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        experience INTEGER,
        fees INTEGER,
        image TEXT,
        about TEXT
    )
    """)

    # ==========================
    # Appointments Table
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(patient_id) REFERENCES patients(id),
        FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    )
    """)

    # ==========================
    # Admin Table
    # ==========================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ==========================
    # Default Admin
    # ==========================
    admin = cursor.execute(
        "SELECT * FROM admins WHERE username=?",
        ("admin",)
    ).fetchone()

    if admin is None:
        cursor.execute("""
        INSERT INTO admins(username,password)
        VALUES(?,?)
        """, (
            "admin",
            generate_password_hash("admin123")
        ))

    # ==========================
    # Sample Doctors
    # ==========================
    doctors = cursor.execute(
        "SELECT COUNT(*) FROM doctors"
    ).fetchone()[0]

    if doctors == 0:

        sample_doctors = [

            (
                "Dr. Rahul Sharma",
                "Orthodontist",
                10,
                500,
                "doctor1.jpg",
                "Specialist in braces and teeth alignment."
            ),

            (
                "Dr. Priya Patel",
                "Dentist",
                8,
                400,
                "doctor2.jpg",
                "Expert in root canal treatment and fillings."
            ),

            (
                "Dr. Amit Kulkarni",
                "Oral Surgeon",
                15,
                700,
                "doctor3.jpg",
                "Experienced oral and maxillofacial surgeon."
            ),

            (
                "Dr. Sneha Deshmukh",
                "Pediatric Dentist",
                6,
                450,
                "doctor4.jpg",
                "Provides dental care for children."
            )

        ]

        cursor.executemany("""
        INSERT INTO doctors(
            name,
            specialization,
            experience,
            fees,
            image,
            about
        )
        VALUES(?,?,?,?,?,?)
        """, sample_doctors)

    conn.commit()
    conn.close()

    print("Database created successfully!")
    print("Default Admin Login")
    print("Username : admin")
    print("Password : admin123")


if __name__ == "__main__":
    create_database()