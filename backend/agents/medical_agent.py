from groq import Groq
from rag.retriever import retrieve_context, build_prompt
from translation.translator import detect_language, translate_from_english
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def medical_chat(user_message: str, session_id: str, language: str = "auto"):
    if language == "auto":
        language = detect_language(user_message)
    
    context = retrieve_context(user_message, language)
    prompt = build_prompt(user_message, context, language)
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are MediTrace AI, a helpful multilingual medical assistant. Always be empathetic, clear, and add medical disclaimers."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024
    )
    
    ai_response = response.choices[0].message.content
    final_response = translate_from_english(ai_response, language)
    
    return {
        "response": final_response,
        "language": language,
        "context_used": context[:200] + "..." if len(context) > 200 else context
    }

def analyze_report(extracted_text: str, language: str = "en"):
    prompt = f"""Analyze this medical report and explain it in simple terms.
Highlight: key findings, normal/abnormal values, and recommendations.
Report:
{extracted_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are MediTrace AI. Explain medical reports in simple, easy to understand language. Always add disclaimer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=1024
    )
    
    ai_response = response.choices[0].message.content
    return translate_from_english(ai_response, language)