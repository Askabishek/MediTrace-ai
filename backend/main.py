from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat, voice, report
from database.models import create_tables

app = FastAPI(title="MediTrace AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat")
app.include_router(voice.router, prefix="/voice")
app.include_router(report.router, prefix="/report")

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"message": "MediTrace AI Backend Running!"}
