from app.db import db


class BlockedRecipe(db.Model):
    __tablename__ = "blocked_recipes"

    utilizador_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receita_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

    __table_args__ = (db.PrimaryKeyConstraint("utilizador_id", "receita_id"),)

    def __repr__(self):
        return f"<BlockedRecipe user:{self.utilizador_id} receita:{self.receita_id}>"
