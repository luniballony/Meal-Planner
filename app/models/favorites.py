from app.db import db


class Favorites(db.Model):
    __tablename__ = "favorites"

    utilizador_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receita_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)

    def __repr__(self):
      return f"<User:{self.utilizador_id} Recipe id:{self.receita_id}>"

    def to_dict(self):
        return {
            "id_receita": self.receita_id,
            "id_utilizador": self.utilizador_id,
        }
  
    # impede que utilizador adicione a mesma receita várias vezes
    __table_args__ = (
    db.PrimaryKeyConstraint('utilizador_id', 'receita_id'),
)


