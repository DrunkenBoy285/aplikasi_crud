# ============================================================
# routers/profile.py
# Read file created.
# Buat handler Update dan Delete juga di sini!
# ============================================================

import os
import uuid
from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Folder upload
UPLOAD_DIR = "static/uploads"


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