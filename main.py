from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import DATABASE_URI, JWT_SECRET_KEY
from db import db
from routes.auth import auth_bp
from routes.dsrt import dsrt_bp
from routes.isian import isian_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# register blueprint
app.register_blueprint(auth_bp,url_prefix='/api')
app.register_blueprint(dsrt_bp)
app.register_blueprint(isian_bp)

if __name__ == '__main__':
    app.run(debug=True)

