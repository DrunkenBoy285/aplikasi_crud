from fastapi import (
    APIRouter,
    Request,
    Depends,
    Form,
    UploadFile,
    File,
    HTTPException
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from flask import request
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Barang

import os
import shutil
import uuid

router = APIRouter(prefix="/inventaris", tags=["Inventaris"])

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================
# Database
# ==========================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# Halaman Inventaris
# ==========================

@router.get("/")
def inventaris(
    request: Request,
    db: Session = Depends(get_db)
):
    barang = db.query(Barang).all()

    return templates.TemplateResponse(
        "datainventaris.html",
        {
            "request": request,
            "barang_list": barang
        }
    )


# ==========================
# Tambah Barang
# ==========================

@router.post("/create")
async def create_barang(
    nama_barang: str = Form(...),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    existing = db.query(Barang).filter(
        Barang.nama_barang == nama_barang
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Nama barang sudah digunakan."
        )

    filename = None

    if photo and photo.filename != "":
        ext = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

    barang = Barang(
        nama_barang=nama_barang,
        photo_barang=filename
    )

    db.add(barang)
    db.commit()

    return RedirectResponse(
        "/inventaris/",
        status_code=303
    )


# ==========================
# Edit Barang
# ==========================

@router.post("/edit/{id_barang}")
async def edit_barang(
    id_barang: int,
    nama_barang: str = Form(...),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    barang = db.query(Barang).filter(
        Barang.id_barang == id_barang
    ).first()

    if not barang:
        raise HTTPException(
            status_code=404,
            detail="Barang tidak ditemukan."
        )

    barang.nama_barang = nama_barang

    if photo and photo.filename != "":

        if barang.photo_barang:
            old_file = os.path.join(
                UPLOAD_FOLDER,
                barang.photo_barang
            )

            if os.path.exists(old_file):
                os.remove(old_file)

        ext = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        barang.photo_barang = filename

    db.commit()

    return RedirectResponse(
        "/inventaris/",
        status_code=303
    )


# ==========================
# Hapus Barang
# ==========================

@router.post("/delete/{id_barang}")
def delete_barang(
    id_barang: int,
    db: Session = Depends(get_db)
):

    barang = db.query(Barang).filter(
        Barang.id_barang == id_barang
    ).first()

    if not barang:
        raise HTTPException(
            status_code=404,
            detail="Barang tidak ditemukan."
        )

    if barang.photo_barang:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            barang.photo_barang
        )

        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(barang)
    db.commit()

    return RedirectResponse(
        "/inventaris/",
        status_code=303
    )