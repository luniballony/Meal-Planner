from app import create_app
from app.db import db

# Importar modelos para que SQLAlchemy os reconheça
from app.models import user, recipe, meal_plan

app = create_app()

with app.app_context():
    print("🛠️ A criar a base de dados...")
    db.create_all()
    print("✅ Base de dados criada com sucesso.")
