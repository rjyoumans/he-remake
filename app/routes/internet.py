from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Computer, InstalledSoftware, Server, Software, User

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
    error = request.query_params.get("error")
    success = request.query_params.get("success")

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
            "error": error,
            "success": success,
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

@router.post("/download")
def download_software(
    request: Request,
    ip: str = Form(...),
    software_id: int = Form(...),
    db: Session = Depends(get_db),
):
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/auth/login", status_code=302)

    server_sessions = request.session.get("server_sessions", {})

    if not server_sessions.get(ip, False):
        return RedirectResponse(url=f"/internet/?ip={ip}&tab=login", status_code=302)

    computer = db.query(Computer).filter(Computer.user_id == user_id).first()
    software = db.query(Software).filter(Software.id == software_id).first()

    if not computer or not software:
        return RedirectResponse(url=f"/internet/?ip={ip}&tab=software", status_code=302)

    existing_install = db.query(InstalledSoftware).filter(
        InstalledSoftware.computer_id == computer.id,
        InstalledSoftware.software_id == software.id,
    ).first()

    if existing_install:
        return RedirectResponse(
            url=f"/internet/?ip={ip}&tab=software",
            status_code=302,
        )

    installed_software_list = db.query(InstalledSoftware).filter(
        InstalledSoftware.computer_id == computer.id
    ).all()

    used_storage = sum(
        installed.software.size for installed in installed_software_list
    )

    if used_storage + software.size > computer.storage_capacity:
        return RedirectResponse(
            url=f"/internet/?ip={ip}&tab=software&error=storage",
            status_code=302,
        )

    installed_software = InstalledSoftware(
        computer_id=computer.id,
        software_id=software.id,
    )
    db.add(installed_software)
    db.commit()

    return RedirectResponse(url=f"/internet/?ip={ip}&tab=software", status_code=302)
