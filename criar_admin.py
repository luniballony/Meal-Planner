from app import create_app
from app.db import db
from app.models.user import User

app = create_app()

with app.app_context():
    nome = "Admin"
    email = "admin@mealplanner.com"
    password = "admin123"

    # Verificar se já existe
    admin_existente = User.query.filter_by(email=email).first()
    if admin_existente:
        print("❌ Já existe um administrador com esse email.")
    else:
        admin = User(nome=nome, email=email, nivel=3)  # nível 3 = admin
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("✅ Administrador criado com sucesso!")
