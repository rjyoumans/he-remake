from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, internet, home
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")  # Replace with a secure key in production

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(internet.router)
