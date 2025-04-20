from flask import Blueprint, request, jsonify
from models import db, User
from passlib.hash import sha256_crypt
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ["POST"])
def register():
    data  = request.get_json()
    hashed_pw = sha256_crypt.hash(data['password'])
    new_user = User(email=data['email'], password = hashed_pw, role = data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    new_user = User.query.filter_by(email = data['email']).first()
    if new_user and sha256_crypt.verify(data['password'], new_user.password):
        access_token = create_access_token(identity={"id": new_user.id, "role": new_user.role})
        return jsonify(access_token = access_token)
    return jsonify({"message": "Invalid Credentials"}), 401
