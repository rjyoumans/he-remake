from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Computer, IPAddress
from app.security import hash_password, verify_password
import random

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
    
    request.session["user_id"] = user.id
    return RedirectResponse("/home/", status_code=303)
            
@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username or email already exists"})
    
    new_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(new_user)
    db.flush()

    new_computer = Computer(
        user_id=new_user.id
    )

    db.add(new_computer)
    db.flush()

    starting_ip = IPAddress(
        address=f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}",
        computer_id=new_computer.id
    )

    db.add(starting_ip)
    db.commit()

    db.refresh(new_user)

    return RedirectResponse("/auth/login", status_code=303)

@router.get("/logout")
def logout_user(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse("/auth/login", status_code=303)