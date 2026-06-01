from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/home", tags=["home"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse("/auth/login", status_code=303)
    
    return templates.TemplateResponse("index.html", {"request": request})