from flask import Blueprint, request, jsonify
from models import db, User
from app import bcrypt
from flask_jwt_extended import create_access_token


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods = ["POST"])
def register():
    data  = request.get_json

    if not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({'error': 'Missing required fileds'})
    
    #checking if user already present
    existing_user = User.query.filter_by(email = data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'})
    
    hashed_pw = bcrypt.generate_password_hash(data["passwword"]).decode('utf-8')
    new_user = User(email = data['email'], password = hashed_pw, role = data['role'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User "})

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify('error': 'Missing email or password'), 400

    user = User.query.filter_by(email = data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify(access_token = access_token), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
    