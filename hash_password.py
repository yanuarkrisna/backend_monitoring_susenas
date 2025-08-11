from werkzeug.security import generate_password_hash
from db import db
from model import User
from main import app  # pastikan app sudah ada

with app.app_context():
    # Ganti "gumri" ini ke username yang mau di-hash passwordnya
    user = User.query.filter_by(username="gumri").first()
    if user:
        user.password_hash = generate_password_hash("gumri")
        db.session.commit()
        print("Password untuk user gumri sudah di-hash.")
    else:
        print("User tidak ditemukan.")
