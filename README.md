Hospital Management System
This Hospital Management System (HMS) is built using Flask with SQLite as the database. The system is designed to streamline hospital management operations, including managing patient records, ward allocations, appointments, and doctor information.

Table of Contents
Features
Technologies Used
Installation
Usage
Image Upload
Team Members
Features
Patient Management: Add, view, and update patient information.
Ward Management: Assign patients to wards and rooms.
Doctor Management: Manage doctor information and specializations.
Appointment Scheduling: Schedule and track appointments with doctors.
Technologies Used
Backend: Flask (Python)
Database: SQLite with SQLAlchemy ORM
Frontend: HTML, CSS, JavaScript
Installation
Clone the repository

bash
Copy code
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system
Install dependencies

Make sure you have Python installed, then install the required packages:

bash
Copy code
pip install -r requirements.txt
Initialize the database

Run the script to set up the initial database structure:

bash
Copy code
python init_db.py
Run the application

Start the Flask server:

bash
Copy code
flask run
Access the application

Open a web browser and go to http://127.0.0.1:5000.

Usage
Add Patients: Use the "Add Patient" form to add new patients to the system.
Manage Wards: Allocate wards and rooms to patients in the "Ward Management" section.
Doctor Information: Add or view doctor details and their specializations.
Schedule Appointments: Schedule appointments between patients and doctors.
Image Upload
To upload images:

Go to the "Image Upload" section in the application.
Select up to 10 images to upload from your local device.
Click "Upload" to add images to the system, which will be associated with the relevant records.
Team Members
Member 1
Member 2
Member 3
Member 4
Member 5
Member 6
