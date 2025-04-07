import os
from dotenv import load_dotenv

# Carregar variáveis do ficheiro .env (apenas em desenvolvimento)
if os.path.exists(".env"):
    load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-padrao")
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY", "csrf-secreto")

    # Ajuste para PostgreSQL no Railway
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///mealplanner.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
