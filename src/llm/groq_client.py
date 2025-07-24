from langchain_groq import ChatGroq
from src.config.settings import settings


# 🧠 Initializes and returns a Groq LLM client using project settings
def get_groq_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,  # API key from .env or settings file
        model=settings.MODEL_NAME,  # Model name, e.g., 'mixtral-8x7b-32768'
        temperature=settings.TEMPERATURE,  # Controls randomness in output
    )
