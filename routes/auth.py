from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import db
from model import User

auth_bp = Blueprint('auth', __name__)

# ===============================
# Register Banyak User Sekaligus
# ===============================
@auth_bp.route('/register_bulk', methods=['POST'])
@jwt_required() 
def register_bulk():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != "Admin":
        return jsonify({"msg": "Hanya admin yang boleh menambah user"}), 403
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"msg": "Data harus berupa array JSON"}), 400

    created_users = []
    skipped_users = []

    for item in data:
        username = item.get("username")
        password = item.get("password")
        nama_lengkap = item.get("nama_lengkap")
        role = item.get("role")
        id_sobat = item.get("id_sobat")
        aktif = item.get("aktif",True)

        if not username or not password:
            skipped_users.append({"username": username, "reason": "Username/Password kosong"})
            continue

        # Cek apakah username sudah ada
        if User.query.filter_by(username=username).first():
            skipped_users.append({"username": username, "reason": "Username sudah ada"})
            continue

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password_hash=hashed_password,
            nama_lengkap=nama_lengkap,
            role=role,
            id_sobat=id_sobat
        )
        db.session.add(new_user)
        created_users.append(username)

    db.session.commit()

    return jsonify({
        "msg": "Proses selesai",
        "berhasil_dibuat": created_users,
        "dilewati": skipped_users
    }), 201


# =======================
# REGISTER USER
# =======================
@auth_bp.route('/register', methods=['POST'])
@jwt_required()  # hanya admin yang boleh
def register():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != "Admin":
        return jsonify({"msg": "Hanya admin yang boleh menambah user"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    nama_lengkap = data.get('nama_lengkap')
    role = data.get('role')
    id_sobat = data.get("id_sobat")
    aktif = data.get('aktif', True)

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username sudah terdaftar"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        password_hash=hashed_password,
        nama_lengkap=nama_lengkap,
        role=role,
        id_sobat=id_sobat,
        aktif=aktif
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User berhasil dibuat"}), 201


# =======================
# LOGIN USER
# =======================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"msg": "Username atau password salah"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "nama": user.nama_lengkap,
        "role": user.role,
        "token": token
    })


# =======================
# LIST SEMUA USER
# =======================
@auth_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = User.query.all()
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "nama_lengkap": u.nama_lengkap,
            "role": u.role,
            "aktif": u.aktif
        })
    return jsonify(data)


# =======================
# HAPUS USER
# =======================
@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if current_user.role != "admin":
        return jsonify({"msg": "Hanya admin yang boleh menghapus user"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User tidak ditemukan"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User berhasil dihapus"})
