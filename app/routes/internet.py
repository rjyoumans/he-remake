from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Server, Software, User

router = APIRouter(prefix="/internet", tags=["internet"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def internet_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    user = db.query(User).filter(User.id == user_id).first()
    ip = request.query_params.get("ip")
    tab = request.query_params.get("tab", "index")

    server_sessions = request.session.get("server_sessions", {})
    logged_in = False
    available_software = []

    server = None
    if ip:
        server = db.query(Server).filter(Server.ip_address == ip).first()

        if server:
            logged_in = server_sessions.get(server.ip_address, False)

            if logged_in and tab == "software":
                available_software = db.query(Software).all()

    return templates.TemplateResponse(
        "internet.html",
        {
            "request": request,
            "user": user,
            "server": server,
            "ip": ip,
            "tab": tab,
            "logged_in": logged_in,
            "available_software": available_software,
        },
    )


# New login route for server authentication
@router.post("/login")
def login_to_server(
    request: Request,
    ip: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=302)

    server = db.query(Server).filter(Server.ip_address == ip).first()

    if not server:
        return RedirectResponse(url=f"/internet/?ip={ip}", status_code=302)

    if username == server.username and password == server.password:
        server_sessions = request.session.get("server_sessions", {})
        server_sessions[server.ip_address] = True
        request.session["server_sessions"] = server_sessions

        return RedirectResponse(
            url=f"/internet/?ip={ip}",
            status_code=302,
        )

    return RedirectResponse(
        url=f"/internet/?ip={ip}&tab=login",
        status_code=302,
    )

@router.get("/logout")
def logout_from_server(
    request: Request,
    ip: str,
):
    server_sessions = request.session.get("server_sessions", {})

    if ip in server_sessions:
        del server_sessions[ip]
    request.session["server_sessions"] = server_sessions

    return RedirectResponse(url=f"/internet/?ip={ip}", status_code=302)