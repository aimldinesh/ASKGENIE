import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = "llama3-70b-8192"

    TEMPERATURE = 0.9

    MAX_RETRIES = 3


settings = Settings()
