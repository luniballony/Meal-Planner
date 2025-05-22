from datetime import datetime, timezone
from app.db import db
from app.models.category import Category


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    instrucoes = db.Column(db.Text, nullable=False)
    tempo_preparacao = db.Column(db.Integer, nullable=False)
    dificuldade = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(150))
    data_submetida = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    publicada = db.Column(db.Boolean, default=False)
    aprovada = db.Column(db.Boolean, default=False)
    fonte = db.Column(db.String(50), default="utilizador")
    # Novo campo para armazenar a preferência do utilizador
    publica_quando_aprovada = db.Column(db.Boolean, default=False)

    utilizador_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    autor = db.relationship("User", backref=db.backref("receitas", lazy=True))

    categoria_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    categoria = db.relationship("Category", backref=db.backref("receitas", lazy=True))

    def __repr__(self):
        return f"<Recipe {self.titulo}>"

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "ingredientes": self.ingredientes,
            "instrucoes": self.instrucoes,
            "tempo_preparacao": self.tempo_preparacao,
            "dificuldade": self.dificuldade,
            "tags": self.tags,
            "publicada": self.publicada,
            "data_submetida": self.data_submetida.isoformat(),
            "fonte": self.fonte,
            "autor_id": self.utilizador_id,
            "categoria_id": self.categoria_id,
        }
