# routes/isian.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from model import IsianDsrt
from db import db

isian_bp = Blueprint('isian', __name__)

@isian_bp.route('/isian', methods=['POST'])
@jwt_required()
def simpan_isian():
    data = request.get_json()
    isian = IsianDsrt(
        dsrt_id = data['dsrt_id'],
        tanggal_pendataan = data['tanggal_pendataan'],
        status = data['status'],
        nama_krt = data['nama_krt'],
        jumlah_art = data['jumlah_art'],
        pengeluaran_makanan = data['pengeluaran_makanan'],
        pengeluaran_nonmakanan = data['pengeluaran_nonmakanan'],
        rata_rata_perkapita = data['rata_rata_perkapita'],
        transportasi = data['transportasi'],
        art_sekolah = data['art_sekolah'],
        art_bpjs = data['art_bpjs'],
        ijazah_krt = data['ijazah_krt'],
        menerima_bantuan = data['menerima_bantuan'],
        jenis_bantuan = data['jenis_bantuan'],
        pendidikan_krt = data['pendidikan_krt'],
        latitude = data['latitude'],
        longitude = data['longitude']
    )
    db.session.add(isian)
    db.session.commit()
    return jsonify({"msg": "Isian DSRT berhasil disimpan"})
