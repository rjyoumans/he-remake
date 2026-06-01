from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, internet, home

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router, prefix="/home", tags=["home"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(internet.router, prefix="/internet", tags=["internet"])
