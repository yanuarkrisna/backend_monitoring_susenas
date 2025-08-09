from flask import Flask
from flask_migrate import Migrate
from config import DATABASE_URI
from db import db
import model  # pastikan model di-import supaya terdaftar di SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # <-- tambahkan ini

@app.route('/')
def home():
    return "Backend Monitoring SUSENAS aktif!"

if __name__ == '__main__':
    app.run(debug=True)
