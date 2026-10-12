import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, report, voice
from database.models import create_tables

app = FastAPI(title="MediTrace AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(report.router, prefix="/report", tags=["Report Analysis"])
app.include_router(voice.router, prefix="/voice", tags=["Voice Transcription"])

@app.on_event("startup")
def startup_event():
    create_tables()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
