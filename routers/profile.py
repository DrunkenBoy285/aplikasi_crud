# ============================================================
# routers/profile.py
# Read file created.
# Buat handler Update dan Delete juga di sini!
# ============================================================

import os
import uuid
import shutil
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from database import get_db
from models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Folder upload
UPLOAD_DIR = "static/uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


# ── Read profile
@router.get("/profile/{user_id}", response_class=HTMLResponse)
def view_profile(user_id: int, request: Request, db: Session = Depends(get_db)):
    # Cari user berdasarkan ID
    # SELECT * FROM users WHERE id = user_id LIMIT 1
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    return templates.TemplateResponse(request, "profile.html", {
        "user": user
    })

# ============================================================
# ===== BARU =====
# Upload Foto Profil
# ============================================================

@router.post("/profile/{user_id}/upload")
async def upload_photo(
    user_id: int,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Validasi ekstensi
    allowed = ["jpg", "jpeg", "png"]

    ext = photo.filename.split(".")[-1].lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail="File harus JPG, JPEG atau PNG"
        )

    # Nama file acak
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    # Simpan file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Hapus foto lama
    if user.photo:
        old_photo = os.path.join(UPLOAD_DIR, user.photo)

        if os.path.exists(old_photo):
            os.remove(old_photo)

    # Simpan nama file ke database
    user.photo = filename

    db.commit()

    return RedirectResponse(
        url=f"/profile/{user.id}",
        status_code=303
    )

# ============================================================
# ===== BARU =====
# Hapus Akun
# ============================================================

@router.post("/profile/{user_id}/delete")
def delete_account(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Hapus foto jika ada
    if user.photo:

        photo_path = os.path.join(
            UPLOAD_DIR,
            user.photo
        )

        if os.path.exists(photo_path):
            os.remove(photo_path)

    db.delete(user)

    db.commit()

    return RedirectResponse(
        url="/",
        status_code=303
    )
# ============================================================
# ===== BARU BANGET =====
@router.post("/profile/{user_id}/update")
def update_profile(
    user_id: int,
    full_name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Update data
    user.full_name = full_name
    user.email = email

    db.commit()

    return RedirectResponse(
        url=f"/profile/{user.id}",
        status_code=303
    )