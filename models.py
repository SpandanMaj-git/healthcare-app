from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(10), nullable = False, default = 'patient')
    is_approved = db.Column(db.Boolean, default=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.String(20), default = "Scheduled") #scheduled, cancelled, completed

    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='patient_appointments')
    patient = db.relationship('User', foreign_keys=[patient_id], backref = 'doctor_appointments')
