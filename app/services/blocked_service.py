from app.db import db
from app.models import BlockedRecipe, Recipe


def bloquear_receita(user_id, receita_id):
    bloqueada = BlockedRecipe.query.filter_by(
        utilizador_id=user_id, receita_id=receita_id
    ).first()
    if not bloqueada:
        nova = BlockedRecipe(utilizador_id=user_id, receita_id=receita_id)
        db.session.add(nova)
        db.session.commit()
        return True
    return False  # já estava bloqueada


def listar_bloqueadas(user_id):
    return (
        db.session.query(Recipe)
        .join(BlockedRecipe, Recipe.id == BlockedRecipe.receita_id)
        .filter(BlockedRecipe.utilizador_id == user_id)
        .all()
    )


def desbloquear_receita(user_id, receita_id):
    bloqueada = BlockedRecipe.query.filter_by(
        utilizador_id=user_id, receita_id=receita_id
    ).first()
    if bloqueada:
        db.session.delete(bloqueada)
        db.session.commit()
        return True
    return False


# acho que de momento não está a ser usada
def listar_nao_bloqueadas(user_id):
    # Obtem os IDs das receitas bloqueadas
    subquery = (
        db.session.query(BlockedRecipe.receita_id)
        .filter(BlockedRecipe.utilizador_id == user_id)
        .subquery()
    )

    # Retorna as receitas que NÃO estão na lista de bloqueadas
    return (
        db.session.query(Recipe)
        .filter(~Recipe.id.in_(subquery))
        .all()
    )