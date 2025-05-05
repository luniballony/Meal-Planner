from app.models.favorites import Favorites
from app.db import db

def adicionar_favorito(user_id, recipe_id):
    favorito = Favorites.query.filter_by(utilizador_id=user_id, receita_id=recipe_id).first()
    if favorito is None:
        novo_favorito = Favorites(utilizador_id=user_id, receita_id=recipe_id)
        db.session.add(novo_favorito)
        db.session.commit()
        return True
    return False  # Já existia nos favoritos

def remover_favorito(user_id, recipe_id):
    favorito = Favorites.query.filter_by(utilizador_id=user_id, receita_id=recipe_id).first()
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return True
    return False  # Não estava nos favoritos
