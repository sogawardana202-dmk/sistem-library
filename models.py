from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='admin')  # only admin

class Buku(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    penulis = db.Column(db.String(100))
    tahun = db.Column(db.String(4))
    deskripsi = db.Column(db.Text, nullable=True)
    foto = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Peminjaman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buku_id = db.Column(db.Integer, db.ForeignKey('buku.id'))
    user_name = db.Column(db.String(100))  # user tidak login, pakai nama
    tanggal_pinjam = db.Column(db.Date)
    jam_pinjam = db.Column(db.Time)
    tanggal_kembali = db.Column(db.Date)
    # Tambahkan relationship
    buku = db.relationship('Buku', backref=db.backref('peminjamans', lazy=True))

class Surat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100))
    pengirim = db.Column(db.String(50))
    penerima = db.Column(db.String(50))
    file = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

