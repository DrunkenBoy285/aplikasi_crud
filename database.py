# ============================================================
# database.py
# File ini bertugas membuat koneksi ke database SQLite
# dan menyediakan "sesi" yang dipakai untuk query data.
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# URL koneksi ke database SQLite
# "sqlite:///./data.db" artinya buat file bernama data.db
# di folder yang sama dengan project kita.
DATABASE_URL = "sqlite:///./data.db"

# Engine adalah "mesin" yang menangani komunikasi ke database.
# connect_args ini khusus SQLite supaya bisa dipakai multi-thread.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal adalah "pabrik" untuk membuat sesi database.
# Setiap request dari user akan dapat satu sesi sendiri.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base adalah kelas induk untuk semua model/tabel kita.
# Setiap tabel yang kita buat harus mewarisi (inherit) dari Base ini.
class Base(DeclarativeBase):
    pass

# Fungsi ini dipanggil setiap kali ada request masuk.
# Tugasnya: buka sesi → kasih ke handler → tutup sesi setelah selesai.
# Kata "yield" membuat ini jadi "generator" — konsep Python lanjutan.
def get_db():
    db = SessionLocal()
    try:
        yield db  # kasih sesi ke fungsi yang meminta
    finally:
        db.close()  # selalu tutup sesi setelah selesai