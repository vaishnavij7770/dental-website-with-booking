import sqlite3

conn = sqlite3.connect("dental.db")
cursor = conn.cursor()

# ---------------- Patients ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT NOT NULL,

age INTEGER NOT NULL,

gender TEXT NOT NULL,

mobile TEXT UNIQUE NOT NULL,

email TEXT UNIQUE NOT NULL,

address TEXT NOT NULL,

password TEXT NOT NULL

)
""")

# ---------------- Doctors ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT NOT NULL,

specialization TEXT NOT NULL,

experience TEXT NOT NULL,

timing TEXT NOT NULL,

fee INTEGER NOT NULL,

image TEXT

)
""")

# ---------------- Appointments ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(

id INTEGER PRIMARY KEY AUTOINCREMENT,

patient_id INTEGER,

doctor_id INTEGER,

treatment TEXT,

appointment_date TEXT,

appointment_time TEXT,

status TEXT DEFAULT 'Pending',

FOREIGN KEY(patient_id) REFERENCES patients(id),

FOREIGN KEY(doctor_id) REFERENCES doctors(id)

)
""")

# ---------------- Insert Doctors ----------------

cursor.execute("SELECT COUNT(*) FROM doctors")

count = cursor.fetchone()[0]

if count == 0:

    doctors = [

        (
            "Dr. Priya Sharma",
            "Orthodontist",
            "8 Years",
            "10 AM - 4 PM",
            500,
            "doctor1.jpg"
        ),

        (
            "Dr. Rahul Mehta",
            "Dental Surgeon",
            "10 Years",
            "11 AM - 6 PM",
            600,
            "doctor2.jpg"
        ),

        (
            "Dr. Sneha Patil",
            "Cosmetic Dentist",
            "6 Years",
            "9 AM - 2 PM",
            450,
            "doctor3.jpg"
        )

    ]

    cursor.executemany("""

    INSERT INTO doctors
    (name,specialization,experience,timing,fee,image)

    VALUES(?,?,?,?,?,?)

    """, doctors)

conn.commit()

conn.close()

print("Database Created Successfully")