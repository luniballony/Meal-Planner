import os
from dotenv import load_dotenv

# Carregar variáveis do ficheiro .env
load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-padrao")
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY", "csrf-secreto")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mealplanner.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
