from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.Integer, default=1)  # 1: comum, 2: premium, 3: admin
    ativo = db.Column(db.Boolean, default=True)  # Novo campo
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.nivel == 3

    def is_premium(self):
        return self.nivel == 2

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "nivel": self.nivel,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(),
        }

    def __repr__(self):
        return f"<User {self.email} (Nível: {self.nivel}, Ativo: {self.ativo})>"
