# models.py
import datetime
from sqlalchemy import Column
from db import db

# ===============================
# 1. User & Hak Akses
# ===============================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    nama_lengkap = db.Column(db.String(100))
    role = db.Column(db.String(20))  # admin / petugas
    aktif = db.Column(db.Boolean, default=True)


class UserWilayah(db.Model):
    __tablename__ = 'user_wilayah'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    wilayah_kode = db.Column(db.String(20), db.ForeignKey('wilayah.kode'))


# ===============================
# 2. Wilayah (hierarki)
# ===============================
class Wilayah(db.Model):
    __tablename__ = 'wilayah'
    kode = db.Column(db.String(20), primary_key=True)
    nama = db.Column(db.String(100))
    tingkat = db.Column(db.String(20))
    induk_kode = db.Column(db.String(20), db.ForeignKey('wilayah.kode'))
    # self-referential FK untuk hierarki wilayah


# ===============================
# 3. DSRT (Daftar Sampel Rumah Tangga)
# ===============================
class Dsrt(db.Model):
    __tablename__ = 'dsrt'
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.Integer)
    nks = db.Column(db.String(20))
    nama_krt = db.Column(db.String(100))
    status = db.Column(db.String(20))
    progres = db.Column(db.Integer, default=0)
    tanggal_survey = db.Column(db.Date)
    petugas_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relasi ke IsianDsrt (One-to-One)
    isian = db.relationship("IsianDsrt", backref="dsrt", uselist=False)

# ===============================
# 4. Isian DSRT (hasil wawancara)
# ===============================
class IsianDsrt(db.Model):
    __tablename__ = 'isian_dsrt'
    id = db.Column(db.Integer, primary_key=True)
    dsrt_id = db.Column(db.Integer, db.ForeignKey('dsrt.id'), unique=True)

    # Variabel rumah tangga
    jumlah_art = db.Column(db.Integer)
    pengeluaran_makanan = db.Column(db.Float)
    pengeluaran_nonmakanan = db.Column(db.Float)
    rata_rata_perkapita = db.Column(db.Float)  # aman untuk angka desimal
    transportasi = db.Column(db.String(100))
    art_sekolah = db.Column(db.Integer)
    art_bpjs = db.Column(db.Integer)
    pendidikan_krt = db.Column(db.String(50))
    
    # Info bantuan
    menerima_bantuan = db.Column(db.Boolean)
    jenis_bantuan = db.Column(db.String(255))  # Simpan list bantuan dalam 1 kolom, pisah koma

    #kelistrikan
    pakai_listrik = db.Column(db.Boolean)
    jenis_bayar_listrik = db.Column(db.String(255))
    daya_listrik = db.Column(db.String(255))
    kwh_listrik = db.Column(db.Float)
    pengeluaran_listrik = db.Column(db.Float)

    #perumahan
    status_rumah = db.Column(db.String(255))
    luas_lantai = db.Column(db.Float)


# ===============================
# 6. Foto DSRT
# ===============================
class FotoDsrt(db.Model):
    __tablename__ = 'foto_dsrt'
    id = db.Column(db.Integer, primary_key=True)
    dsrt_id = db.Column(db.Integer, db.ForeignKey('dsrt.id'))
    url_foto = db.Column(db.Text)
    keterangan = db.Column(db.Text)
    waktu_upload = db.Column(db.DateTime)


# ===============================
# 7. Log Aktivitas
# ===============================
class LogAktivitas(db.Model):
    __tablename__ = 'log_aktivitas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    aktivitas = db.Column(db.Text)
    waktu_mulai = db.Column(db.DateTime, default=datetime.UTC)  # waktu mulai otomatis saat insert
    waktu_selesai = db.Column(db.DateTime, nullable=True)          # waktu selesai diisi nanti
    lokasi = db.Column(db.String(100))
    foto_bukti = db.Column(db.Text)


# ===============================
# 8. Progres Harian Petugas
# ===============================
class ProgresHarian(db.Model):
    __tablename__ = 'progres_harian'
    id = db.Column(db.Integer, primary_key=True)
    petugas_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tanggal = db.Column(db.Date)
    jumlah_dsrt = db.Column(db.Integer)
    jumlah_selesai = db.Column(db.Integer)
    catatan = db.Column(db.Text)
