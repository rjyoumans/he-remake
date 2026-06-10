from fastapi import APIRouter, Request, Depends 
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

router = APIRouter(prefix="/internet", tags=["internet"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def internet_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    user = db.query(User).filter(User.id == user_id).first()

    return templates.TemplateResponse(
        "internet.html",
        {
            "request": request,
            "user": user,
        },
    )