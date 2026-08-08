from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from agents.medical_agent import analyze_report
from database.models import get_db, ReportAnalysis
import pdfplumber
import tempfile
import os
import uuid

router = APIRouter()

@router.post("/analyze")
async def analyze_medical_report(
    file: UploadFile = File(...),
    session_id: str = Form(None),
    language: str = Form("en"),
    db: Session = Depends(get_db)
):
    session_id = session_id or str(uuid.uuid4())
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        extracted_text = ""
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""
        if not extracted_text.strip():
            return {"error": "Could not extract text from PDF"}
        summary = analyze_report(extracted_text=extracted_text, language=language)
        report_record = ReportAnalysis(
            session_id=session_id,
            filename=file.filename,
            extracted_text=extracted_text[:1000],
            ai_summary=summary
        )
        db.add(report_record)
        db.commit()
        return {
            "session_id": session_id,
            "filename": file.filename,
            "summary": summary,
            "language": language
        }
    finally:
        os.unlink(tmp_path)

@router.get("/history/{session_id}")
def get_report_history(session_id: str, db: Session = Depends(get_db)):
    reports = db.query(ReportAnalysis).filter(
        ReportAnalysis.session_id == session_id
    ).all()
    return reports