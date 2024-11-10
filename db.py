from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import event

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

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



