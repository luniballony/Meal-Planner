from app.models.category import Category
from app.db import db


def listar_categorias():
    return Category.query.order_by(Category.nome.asc()).all()


def obter_categoria_por_id(categoria_id):
    return Category.query.get(categoria_id)


def criar_categoria(nome):
    nome = nome.strip().title()
    if not nome:
        return None

    existente = Category.query.filter_by(nome=nome).first()
    if existente:
        return existente

    nova = Category(nome=nome)
    db.session.add(nova)
    db.session.commit()
    return nova


def eliminar_categoria(id):
    categoria = obter_categoria_por_id(id)
    if categoria and not categoria.receitas:
        db.session.delete(categoria)
        db.session.commit()
        return True
    return False


def editar_categoria(id, novo_nome):
    categoria = obter_categoria_por_id(id)
    if categoria is not None:
        categoria.nome = novo_nome.strip().title()
        db.session.commit()
        return categoria
    return None
