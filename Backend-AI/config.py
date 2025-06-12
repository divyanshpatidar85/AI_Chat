import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

DB_CONFIG = {
    "server": os.getenv("DB_SERVER"),
    "database": os.getenv("DB_NAME"),
    "username": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "driver": "{ODBC Driver 17 for SQL Server}"
}

GENAI_API_KEY = os.getenv("GENAI_API_KEY")
