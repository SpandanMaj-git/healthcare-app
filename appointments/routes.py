from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Appointment
from extensions import db
from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)


#endpoint for booking an appointment
@appointments_bp.route('/book', methods =["POST"])
@jwt_required
def book_appointments():
    data = request.get_json()
    current_user = get_jwt_identity()

    doctor = User.query.filter_by(id = data['doctor_id'], role='doctor').first()
    if not doctor:
        return jsonify({'error':"invalid doctor id"})
    

    #check if doctor already has an appointment at the given date and time
    existing = Appointment.query.filter_by(
        doctor_id = data['doctor_id'],
        date = datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time = datetime.strptime(data['time'], '%H-%M').time()
    ).first()

    if existing:
        return jsonify({'error': 'Doctor already has an appointment at thist time'})
    

#to view upcoming appointments
@appointments_bp.route('/upcoming')
@jwt_required
def view_upcoming_appointments():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    now = datetime.utcnow()
    appointments = []

    if user.role == "doctor":
        appointments = Appointment.query.filter_by(doctor_id = user_id).filter(Appointment.date >= now.date()).all
    elif user.role == 'patient':
        appointments = Appointment.query.filter_by(patient_id = user_id).filter(Appointment.date >= now.date()).all
    else:
        return jsonify({"error": 'invalid user role'}), 403
    
    return jsonify([{
        "id": a.id,
        "date": a.date.isoformat(),
        "time": a.time.strftime('%H:%M'),
        "doctor_id": a.doctor_id,
        "patient_id": a.patient_id,
        "status": a.status
    } for a in appointments]), 200

@appointments_bp.route("/appointments/<int:appt_id>/update", methods=["PUT"])
@jwt_required()
def update_appointment(appt_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()

    appt = Appointment.query.get(appt_id)

    if not appt:
        return jsonify({"msg": "Appointment not found"}), 404
    
    if user.id not in [appt.patient_id, appt.doctor_id]:
        return jsonify({"msg": "Unauthorized"}), 403

    if "action" in data and data["action"] == "cancel":
        appt.status = "cancelled"
        db.session.commit()
        return jsonify({"msg": "Appointment cancelled"}), 200

    elif "new_datetime" in data:
        new_time = datetime.fromisoformat(data["new_datetime"])
        conflict = Appointment.query.filter_by(doctor_id=appt.doctor_id, datetime=new_time, status="confirmed").first()
        if conflict:
            return jsonify({"msg": "Time slot already booked"}), 409

        appt.datetime = new_time
        db.session.commit()
        return jsonify({"msg": "Appointment rescheduled"}), 200

    return jsonify({"msg": "Invalid request"}), 400

    

    
    





    new_appt = Appointment(
        patient_id = current_user,
        doctor_id = data['doctor_id'],
        date = datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time = datetime.strptime(data['time'], '%H:%M').time()
    )
    db.session.add(new_appt)
    db.session.commit()

    return jsonify({'message': 'appointment booked'})