from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from auth.routes import auth_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)




#############################################################








