from db import db
from datetime import datetime

# ===============================
# 1. User
# ===============================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    nama_lengkap = db.Column(db.String(100))
    role = db.Column(db.String(20))
    id_sobat = db.Column(db.String(20))
    aktif = db.Column(db.Boolean, default=True)

# ===============================
# 2. Struktur Wilayah Baru
# ===============================
class Kecamatan(db.Model):
    __tablename__ = 'kecamatan'
    id = db.Column(db.Integer, primary_key=True)
    kode_kec = db.Column(db.String(10), unique=True, nullable=False)
    nama_kec = db.Column(db.String(100), nullable=False)
    desa_list = db.relationship('Desa', backref='kecamatan', cascade="all, delete-orphan")

class Desa(db.Model):
    __tablename__ = 'desa'
    id = db.Column(db.Integer, primary_key=True)
    kode_desa = db.Column(db.String(10), unique=True, nullable=False)
    nama_desa = db.Column(db.String(100), nullable=False)
    kode_kec = db.Column(db.String(10), db.ForeignKey('kecamatan.kode_kec'))
    blok_sensus_list = db.relationship('BlokSensus', backref='desa', cascade="all, delete-orphan")

class BlokSensus(db.Model):
    __tablename__ = 'blok_sensus'
    id = db.Column(db.Integer, primary_key=True)
    kode_bs = db.Column(db.String(15), unique=True, nullable=False)
    nks = db.Column(db.String(6), unique=True, nullable=False)
    kode_desa = db.Column(db.String(10), db.ForeignKey('desa.kode_desa'))
    dsrt_list = db.relationship('Dsrt', backref='blok_sensus', cascade="all, delete-orphan")

# ===============================
# 3. DSRT & Isian
# ===============================
class Dsrt(db.Model):
    __tablename__ = 'dsrt'
    id = db.Column(db.Integer, primary_key=True)
    tahun = db.Column(db.Integer)
    petugas_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    kode_bs = db.Column(db.String(15), db.ForeignKey('blok_sensus.kode_bs'))
    nks = db.Column(db.String(6), db.ForeignKey('blok_sensus.nks'))
    no_urut = db.Column(db.Integer)

class IsianDsrt(db.Model):
    __tablename__ = 'isian_dsrt'
    id = db.Column(db.Integer, primary_key=True)
    dsrt_id = db.Column(db.Integer, db.ForeignKey('dsrt.id'), unique=True)
    tanggal_pendataan = db.Column(db.Date)
    status = db.Column(db.String(20))
    nama_krt = db.Column(db.String(100))
    jumlah_art = db.Column(db.Integer)
    pengeluaran_makanan = db.Column(db.Integer)
    pengeluaran_nonmakanan = db.Column(db.Integer)
    rata_rata_perkapita = db.Column(db.Float)
    transportasi = db.Column(db.String(100))
    art_sekolah = db.Column(db.Integer)
    art_bpjs = db.Column(db.Integer)
    ijazah_krt = db.Column(db.String(50))
    menerima_bantuan = db.Column(db.Boolean)
    jenis_bantuan = db.Column(db.String(255))  # simpan list bantuan dipisah koma
    pendidikan_krt = db.Column(db.String(50))
    latitude = db.Column(db.Float)    # koordinat tagging
    longitude = db.Column(db.Float)

# ===============================
# 4. Foto DSRT
# ===============================
class FotoDsrt(db.Model):
    __tablename__ = 'foto_dsrt'
    id = db.Column(db.Integer, primary_key=True)
    dsrt_id = db.Column(db.Integer, db.ForeignKey('dsrt.id'))
    url_foto = db.Column(db.Text)
    keterangan = db.Column(db.Text)
    waktu_upload = db.Column(db.DateTime, default=datetime.utcnow)

# ===============================
# 5. Log Aktivitas
# ===============================
class LogAktivitas(db.Model):
    __tablename__ = 'log_aktivitas'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    aktivitas = db.Column(db.Text)
    waktu_mulai = db.Column(db.DateTime, default=datetime.utcnow)
    waktu_selesai = db.Column(db.DateTime)
    lokasi = db.Column(db.String(100))
    foto_bukti = db.Column(db.Text)

# ===============================
# 6. Progres Harian
# ===============================
class ProgresHarian(db.Model):
    __tablename__ = 'progres_harian'
    id = db.Column(db.Integer, primary_key=True)
    petugas_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tanggal = db.Column(db.Date)
    jumlah_dsrt = db.Column(db.Integer)
    jumlah_selesai = db.Column(db.Integer)
    catatan = db.Column(db.Text)
