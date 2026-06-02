from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter(prefix="/home", tags=["home"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse("/auth/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
            "computer": user.computer if user else None
        }
    )