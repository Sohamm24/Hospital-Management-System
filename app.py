from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import secrets
import string

app = Flask(__name__)
app.secret_key = 'HMS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'

db = SQLAlchemy(app)


users = {
    'doctor': {'username': 'doc1', 'password': 'pass123'},
    'patient': {'username': 'pat1', 'password': 'pass123'},
    'management': {'username': 'man1', 'password': 'pass123'}
}

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    experience = db.Column(db.Integer, nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    problems = db.Column(db.String(100), nullable=False)
    reason_for_admission = db.Column(db.String(200), nullable=False)
    consulting_doctor = db.Column(db.String(100), nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=True)
    relationship_with_patient = db.Column(db.String(50), nullable=True)
    additional_notes = db.Column(db.String(200), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)


with app.app_context():
 db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'doctor':
            return redirect(url_for('doctor_login'))
        elif role == 'patient':
            return redirect(url_for('patient_login'))
        elif role == 'management':
            return redirect(url_for('management_login'))
    return render_template('login.html')

@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users['doctor']['username'] and password == users['doctor']['password']:
            return redirect(url_for('doctor_dashboard'))
        else:
            return "Invalid credentials for Doctor"
    return render_template('login_form.html', role="Doctor")

@app.route('/patient_login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users['patient']['username'] and password == users['patient']['password']:
            return redirect(url_for('patient_dashboard'))
        else:
            return "Invalid credentials for Patient"
    return render_template('login_form.html', role="Patient")

@app.route('/management_login', methods=['GET', 'POST'])
def management_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == users['management']['username'] and password == users['management']['password']:
            return redirect(url_for('management_dashboard'))
        else:
            return "Invalid credentials for Management"
    return render_template('login_form.html', role="Management")


@app.route('/doctor_dashboard')
def doctor_dashboard():
    return "Welcome to Doctor's Dashboard"


@app.route('/management_dashboard')
def management_dashboard():
    return  render_template('management.html')

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
        if request.method == 'POST':
            # Extract form data
            doctor_name = request.form.get('doctorName')
            specialization = request.form.get('specialization')
            email = request.form.get('email')
            phone = request.form.get('phone')
            experience = request.form.get('experience')

            # Check for existing doctor with the same email or specialization
            existing_doctor = Doctor.query.filter(
                (Doctor.email == email) | (Doctor.specialization == specialization)
            ).first()
            if existing_doctor:
                flash("A doctor with this email or specialization already exists.", "danger")
                return redirect(url_for('add_doctor'))

            # Create a new doctor record
            new_doctor = Doctor(
                name=doctor_name,
                specialization=specialization,
                email=email,
                phone=phone,
                experience=experience
            )

            # Add to the database
            db.session.add(new_doctor)
            db.session.commit()
            flash("Doctor added successfully!", "success")
            return redirect(url_for('management_dashboard'))
        
        return render_template('addDoctor.html')

@app.route('/patient_detail',methods=['GET','POST'])
def patient_detail():
 return render_template('general_ward.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        sex = request.form.get('sex')
        problems = request.form.get('problems')
        reason_for_admission = request.form.get('reason')
        consulting_doctor = request.form.get('consulting_doctor')
        emergency_contact = request.form.get('emergency_contact')
        relationship_with_patient = request.form.get('relationship_with_patient')
        additional_notes = request.form.get('additional_notes')

        print(f"Patient Name: {patient_name}, Age: {age}, Sex: {sex}, Problems: {problems}, Reason: {reason_for_admission}")

        # Validation checks
        if not patient_name or not age or not sex or not consulting_doctor:
            flash("Patient name, age, sex, and consulting doctor are required.", "danger")
            return redirect(url_for('add_patient'))

        # Find the consulting doctor
        doctor = Doctor.query.filter_by(name=consulting_doctor).first()
        if not doctor:
            flash("Consulting doctor not found. Please check the name and try again.", "danger")
            return redirect(url_for('add_patient'))

        # Create a new Patient record
        new_patient = Patient(
            name=patient_name,
            age=int(age),
            sex=sex,
            problems=problems,
            reason_for_admission=reason_for_admission,
            consulting_doctor=consulting_doctor,
            emergency_contact=emergency_contact,
            relationship_with_patient=relationship_with_patient,
            additional_notes=additional_notes,
            doctor_id=doctor.id
        )

        # Attempt to add to the database
        try:
            db.session.add(new_patient)
            db.session.commit()
            flash("Patient added successfully!", "success")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            flash(f"Error adding patient: {str(e)}", "danger")
        
        return redirect(url_for('management_dashboard'))

    # Render the form for adding a patient
    return render_template('general_ward.html')  # This should be your form template


if __name__ == '__main__':
      app.run(debug=True)

