from fastapi import FastAPI
from app.api import chat, incognito, secrets
from app.configs import settings
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(chat.router)
app.include_router(incognito.router)
app.include_router(secrets.router)


@app.get("/health", tags=['health'])
def health():
    return {"status": "ok"}

@app.get("/{name}", tags=['root'])
def root(name):
    return f"Hello! {name}"


