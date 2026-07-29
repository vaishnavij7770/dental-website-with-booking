🦷 DentalCare Clinic Management System

A Full Stack Dental Clinic Management System developed using Python Flask. This application allows patients to register, book appointments online, and manage their profiles, while administrators can efficiently manage doctors and appointments through a dedicated dashboard.

📌 Features
👤 Patient Module
Patient Registration & Login
Secure Authentication
View Doctor Profiles
Book Appointments
Reschedule Appointments
Cancel Appointments
View Appointment History
Update Profile
👨‍💼 Admin Module
Secure Admin Login
Dashboard with Statistics
Add New Doctors
Edit Doctor Details
Delete Doctors
Upload Doctor Images
View Patient Appointments
Approve Appointments
Reject Appointments
🛠️ Tech Stack
Frontend
HTML5
CSS3
JavaScript
Jinja2
Font Awesome
Backend
Python
Flask
Database
SQLite3
Other Libraries
Werkzeug (Password Hashing)
Secure File Upload
📂 Project Structure
DentalCare/
│
├── app.py
├── database.py
├── create_db.py
├── requirements.txt
├── dental.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── images/
│       ├── banner.jpg
│       ├── doctor1.jpg
│       ├── doctor2.jpg
│       ├── doctor3.jpg
│       └── doctor4.jpg
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── doctors.html
│   ├── booking.html
│   ├── appointments.html
│   ├── reschedule.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── add_doctor.html
│   └── edit_doctor.html
│
└── README.md
🚀 Installation
Clone the Repository
git clone https://github.com/yourusername/DentalCare.git
Navigate to the Project
cd DentalCare
Create Virtual Environment
python -m venv venv
Activate Virtual Environment

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Create Database
python create_db.py
Run the Application
python app.py

Open your browser and visit:

http://127.0.0.1:5000
🔐 Default Admin Login

Username

admin

Password

admin123

👩‍💻 Author

Vaishnavi Jadhav

💼 Full Stack Developer
🌐 Passionate about Python, Flask, and Web Development
