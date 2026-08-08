from rag.vectorstore import search_documents
from translation.translator import translate_to_english

def retrieve_context(query: str, language: str = "en"):
    if language != "en":
        english_query = translate_to_english(query, language)
    else:
        english_query = query
    results = search_documents(english_query, n_results=5)
    if not results:
        return "No relevant medical information found."
    context = "\n\n".join(results)
    return context

def build_prompt(query: str, context: str, language: str = "en"):
    language_map = {
        "en": "English",
        "ta": "Tamil",
        "hi": "Hindi",
        "te": "Telugu",
        "ml": "Malayalam"
    }
    response_language = language_map.get(language, "English")
    prompt = f"""You are MediTrace AI, a helpful multilingual medical assistant.
Use the following medical context to answer the user's question.
Always respond in {response_language}.
Add a disclaimer that this is not a substitute for professional medical advice.

Medical Context:
{context}

User Question:
{query}

Response:"""
    return prompt
