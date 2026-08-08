from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text: str):
    try:
        lang = detect(text)
        return lang
    except:
        return "en"

def translate_to_english(text: str, source_lang: str = "auto"):
    try:
        translated = GoogleTranslator(
            source=source_lang,
            target="en"
        ).translate(text)
        return translated
    except:
        return text

def translate_from_english(text: str, target_lang: str = "en"):
    if target_lang == "en":
        return text
    try:
        translated = GoogleTranslator(
            source="en",
            target=target_lang
        ).translate(text)
        return translated
    except:
        return text

def get_supported_languages():
    return {
        "en": "English",
        "ta": "Tamil",
        "hi": "Hindi",
        "te": "Telugu",
        "ml": "Malayalam"
    }