from flask import Flask, render_template, request, redirect, url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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
    ward_id=db.Column(db.Integer,db.ForeignKey('ward.ward_id'),nullable=False)


    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'problems': self.problems,
            'consulting_doctor': self.consulting_doctor,
            'ward_id': self.ward_id
        }

class Ward(db.Model): #base class (db.model)
    ward_id = db.Column(db.Integer, primary_key=True)
    ward_name = db.Column(db.String(10), nullable=False)
    ward_type = db.Column(db.String(50))
    total_beds = db.Column(db.Integer)
    
    beds = db.relationship('Bed', backref='ward', lazy=True)

class Bed(db.Model):
    bed_id = db.Column(db.Integer, primary_key=True)
    ward_id = db.Column(db.Integer, db.ForeignKey('ward.ward_id'), nullable=False)
    bed_number = db.Column(db.String(10))
    status = db.Column(db.String(20), default='available')

class PatientRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.String)
    problems = db.Column(db.Text)
    reason_for_admission = db.Column(db.Text)
    consulting_doctor = db.Column(db.String)
    emergency_contact = db.Column(db.String)
    relationship_with_patient = db.Column(db.String)
    additional_notes = db.Column(db.Text)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    symptoms = db.Column(db.Text)
    prescribed_medicines = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    ward_id = db.Column(db.Integer, db.ForeignKey('ward.ward_id'))


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'problems': self.problems,
            'reason_for_admission': self.reason_for_admission,
            'consulting_doctor': self.consulting_doctor,
            'emergency_contact': self.emergency_contact,
            'relationship_with_patient': self.relationship_with_patient,
            'additional_notes': self.additional_notes,
            'doctor_id': self.doctor_id,
            'symptoms': self.symptoms,
            'prescribed_medicines': self.prescribed_medicines,
            'follow_up_date': self.follow_up_date,
            'ward_id': self.ward_id
        }


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
           
            doctor_name = request.form.get('doctorName')
            specialization = request.form.get('specialization')
            email = request.form.get('email')
            phone = request.form.get('phone')
            experience = request.form.get('experience')

            existing_doctor = Doctor.query.filter(
                (Doctor.email == email) | (Doctor.specialization == specialization)
            ).first()
            if existing_doctor:
                flash("A doctor with this email or specialization already exists.", "danger")
                return redirect(url_for('add_doctor'))

           
            new_doctor = Doctor(
                name=doctor_name,
                specialization=specialization,
                email=email,
                phone=phone,
                experience=experience
            )

            try:
               db.session.add(new_doctor)
               db.session.commit()
               flash("Doctor added successfully!", "success")
               return redirect(url_for('management_dashboard'))
            except Exception as e:
               db.session.rollback() 
               print(f"An error occurred: {str(e)}", "danger")
               return redirect(url_for('add_doctor'))


        return render_template('addDoctor.html')


@app.route('/patient_detail',methods=['GET','POST'])
def patient_detail():
    ward_bed_counts = db.session.query(
        Bed.ward_id, func.count(Bed.bed_id).label('available_beds')
    ).filter(Bed.status == 'available').group_by(Bed.ward_id).all()
    
    ward_bed_counts_dict = {ward_id: count for ward_id, count in ward_bed_counts}
    print(ward_bed_counts_dict)

    return render_template('general_ward.html',ward_bed_counts_dict=ward_bed_counts_dict)


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
        ward_id=request.form.get('ward_id')


        print(f"Patient Name: {patient_name}, Age: {age}, Sex: {sex}, Problems: {problems}, Reason: {reason_for_admission}, Ward Selected:{ward_id}")

       
        if not patient_name or not age or not sex or not consulting_doctor:
            flash("Patient name, age, sex, and consulting doctor are required.", "danger")
            return redirect(url_for('add_patient'))

       
        doctor = Doctor.query.filter_by(name=consulting_doctor).first()
        if not doctor:
            flash("Consulting doctor not found. Please check the name and try again.", "danger")
            return redirect(url_for('add_patient'))

       
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
            doctor_id=doctor.id,
            ward_id=ward_id
        )

        
        try:
            db.session.add(new_patient)
            db.session.commit()
            flash("Patient added successfully!", "success")
        except Exception as e:
            db.session.rollback() 
            flash(f"Error adding patient: {str(e)}", "danger")
        
        return redirect(url_for('management_dashboard'))

   
    return render_template('general_ward.html')  

@app.route('/view_patients', methods=['GET', 'POST'])
def view_patients():
  patients = Patient.query.all()
  return render_template('view_patient.html',patients=patients)

@app.route('/get_patients', methods=['GET'])
def get_patients_data():
    patients = Patient.query.all()
    return jsonify([patient.to_dict() for patient in patients]) 

@app.route('/view_patients_record', methods=['GET', 'POST'])
def view_patients_record():
    patients_record =  PatientRecord.query.all()
    return render_template('view_past_patient.html',patients_record=patients_record)

@app.route('/get_patients_record', methods=['GET'])
def get_patients_data_record():
    patients_record = PatientRecord.query.all()
    return jsonify([patient.to_dict() for patient in patients_record])

if __name__ == '__main__':
      app.run(debug=True)

