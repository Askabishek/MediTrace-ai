from fastapi import APIRouter, UploadFile, File, Form
from agents.medical_agent import medical_chat
from translation.translator import detect_language
import groq
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    session_id: str = Form(None),
    language: str = Form("auto")
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file,
            )
        transcribed_text = transcription.text
        detected_lang = detect_language(transcribed_text)
        result = medical_chat(
            user_message=transcribed_text,
            session_id=session_id or "voice_session",
            language=detected_lang
        )
        return {
            "transcribed_text": transcribed_text,
            "detected_language": detected_lang,
            "response": result["response"]
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        os.unlink(tmp_path)
