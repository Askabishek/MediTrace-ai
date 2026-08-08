from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from agents.medical_agent import medical_chat
from database.models import get_db, ChatHistory
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None
    language: str = "auto"

@router.post("/")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    session_id = request.session_id or str(uuid.uuid4())
    result = medical_chat(
        user_message=request.message,
        session_id=session_id,
        language=request.language
    )
    chat_record = ChatHistory(
        session_id=session_id,
        language=result["language"],
        user_message=request.message,
        ai_response=result["response"]
    )
    db.add(chat_record)
    db.commit()
    return {
        "session_id": session_id,
        "response": result["response"],
        "language": result["language"]
    }

@router.get("/history/{session_id}")
def get_history(session_id: str, db: Session = Depends(get_db)):
    history = db.query(ChatHistory).filter(
        ChatHistory.session_id == session_id
    ).all()
    return history