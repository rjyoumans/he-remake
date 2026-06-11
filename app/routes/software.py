from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Computer, User, InstalledSoftware, Software

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/software", tags=["software"])

@router.get("/")
def software_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    user = db.query(User).filter(User.id == user_id).first()
    computer = db.query(Computer).filter(Computer.user_id == user_id).first()
    installed_software = db.query(InstalledSoftware).filter(InstalledSoftware.computer_id == computer.id).all()
    used_storage = sum(
        installed.software.size for installed in installed_software
    )

    return templates.TemplateResponse(
        "software.html",
        {
            "request": request,
            "user": user,
            "computer": computer,
            "installed_software": installed_software,
            "used_storage": used_storage,
        },
    )
