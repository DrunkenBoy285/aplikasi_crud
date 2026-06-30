# ============================================================
# schemas.py
# Schemas adalah "blueprint" untuk validasi data yang masuk.
# Kalau Models mendefinisikan struktur DATABASE,
# maka Schemas mendefinisikan struktur DATA YANG DIKIRIM USER.
# Kita pakai Pydantic untuk ini.
# ============================================================

from pydantic import BaseModel

# Schema untuk registrasi user baru.
# Data ini yang diharapkan dikirim dari form register.
class UserRegister(BaseModel):
    username: str   # tipe data str = teks
    email: str
    password: str
    full_name: str = ""  # tanda = "" artinya nilai default kosong (opsional)

# Schema untuk login.
# Hanya butuh username dan password.
class UserLogin(BaseModel):
    username: str
    password: str

# Schema untuk edit profil.
# Semua field opsional (ada nilai default None),
# jadi user bisa update sebagian saja.
class UserUpdate(BaseModel):
    full_name: str = None  # None = kosong/tidak diisi
    email: str = None