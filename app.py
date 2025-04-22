from flask import Flask
from flask_migrate import Migrate
from config import Config
from extensions import db, bcrypt, jwt
from auth.routes import auth_bp
from doctor.routes import doctor_bp
from appointments.routes import appointments_bp



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate = Migrate(app,db)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(doctor_bp, url_prefix='/doctor')
app.register_blueprint(appointments_bp, url_prefix='/appointments')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)













