from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Appointment
from extensions import db
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/book', methods = "POST")
def book_appointments():
    data = request.get_json()
    current_user = get_jwt_identity()

    doctor = User.query.filter_by(id = data['doctor_id'], role='doctor').first()
    if not doctor:
        return jsonify({'error':"invalid doctor id"})

    new_appt = Appointment(
        patient_id = current_user(get_jwt_identity),
        doctor_id = data['doctor_id'],
        date = datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time = datetime.strptime(data['time'], '%H:%M').time()
    )
    db.session.add(current_user)
    db.session.commit()

    return jsonify({'message': 'appointment booked'})