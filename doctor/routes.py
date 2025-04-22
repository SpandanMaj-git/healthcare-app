from flask import Blueprint, request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity


doctor_bp = Blueprint('doctor', __name__)


@doctor_bp.route('/dashboard')
@jwt_required()
def doctor_dashboard():
    user = get_jwt_identity()
    if user['role'] != 'doctor':
        return jsonify({"error": "Unauthorized access"})
    return jsonify({"message": "Welcome Doctor"})