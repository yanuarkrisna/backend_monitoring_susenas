# routes/dsrt.py
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model import Dsrt
from db import db

dsrt_bp = Blueprint('dsrt', __name__)

@dsrt_bp.route('/dsrt', methods=['GET'])
@jwt_required()
def get_dsrt():
    current_user = get_jwt_identity()
    dsrt_list = Dsrt.query.filter_by(petugas_id=current_user["id"]).all()

    result = []
    for d in dsrt_list:
        result.append({
            "id": d.id,
            "tahun": d.tahun,
            "kode_bs": d.kode_bs,
            "nks": d.nks,
            "no_urut": d.no_urut
        })
    return jsonify(result)
