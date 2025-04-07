from datetime import datetime
from app.db import db


class MealPlan(db.Model):
    __tablename__ = "meal_plans"

    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com o utilizador
    utilizador_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    utilizador = db.relationship("User", backref=db.backref("planos", lazy=True))


class MealEntry(db.Model):
    __tablename__ = "meal_entries"

    id = db.Column(db.Integer, primary_key=True)
    data_refeicao = db.Column(db.Date, nullable=False)
    refeicao_tipo = db.Column(
        db.String(50), nullable=False
    )  # pequeno almoço, almoço, jantar

    # Relações
    plano_id = db.Column(db.Integer, db.ForeignKey("meal_plans.id"), nullable=False)
    plano = db.relationship(
        "MealPlan",
        backref=db.backref("refeicoes", cascade="all, delete-orphan", lazy=True),
    )

    receita_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    receita = db.relationship("Recipe")

    def __repr__(self):
        return f"<MealEntry {self.data_refeicao} - {self.refeicao_tipo}>"
