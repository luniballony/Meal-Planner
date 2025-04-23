from app.models.recipe import Recipe
from app.db import db
from sqlalchemy import or_
from flask import session


def criar_receita(dados, utilizador_id, publica_quando_aprovada=False):
    titulo = dados.get("titulo", "").strip().title()
    descricao = dados.get("descricao", "").strip()
    ingredientes = dados.get("ingredientes", "").strip()
    instrucoes = dados.get("instrucoes", "").strip()
    tempo = dados.get("tempo_preparacao")
    dificuldade = dados.get("dificuldade")
    tags = dados.get("tags", "").strip()
    categoria_id = dados.get("categoria_id")

    if not (titulo and ingredientes and instrucoes and categoria_id):
        return None  # Campos essenciais obrigatórios

    nova_receita = Recipe(
        titulo=titulo,
        descricao=descricao,
        ingredientes=ingredientes,
        instrucoes=instrucoes,
        tempo_preparacao=tempo,
        dificuldade=dificuldade,
        tags=tags,
        categoria_id=categoria_id,
        publicada=dados.get("publicada", False),
        aprovada=dados.get("aprovada", False),
        fonte=dados.get("fonte", "utilizador"),
        utilizador_id=utilizador_id,
        # Armazenar a preferência do usuário em um campo adicional
        publica_quando_aprovada=publica_quando_aprovada,
    )
    db.session.add(nova_receita)
    db.session.commit()
    return nova_receita


def aprovar_receita(receita_id):
    receita = Recipe.query.get(receita_id)
    if receita:
        # Definir como publicada apenas se o usuário marcou a opção
        receita.publicada = receita.publica_quando_aprovada
        receita.aprovada = True
        db.session.commit()
    return receita


def eliminar_receita(receita_id):
    receita = Recipe.query.get(receita_id)
    if receita:
        db.session.delete(receita)
        db.session.commit()
        return True  # Retorna True quando a operação for bem-sucedida
    return False  # Retorna False se a receita não for encontrada


def listar_receitas():
    user_id = session.get("user_id")
    nivel = session.get("user_nivel")

    query = Recipe.query

    if nivel == 3:
        return query.order_by(Recipe.data_submetida.desc()).all()

    if user_id:
        query = query.filter(
            or_(
                Recipe.publicada == True,
                Recipe.utilizador_id == user_id
            )
        )
    else:
        query = query.filter_by(publicada=True)

    return query.order_by(Recipe.data_submetida.desc()).all()


def buscar_receitas(filtros):
    query = Recipe.query.filter_by(publicada=True)

    if "search" in filtros:
        termo = f"%{filtros['search']}%"
        query = query.filter(
            or_(Recipe.titulo.ilike(termo), Recipe.descricao.ilike(termo))
        )

    if "categoria" in filtros:
        query = query.filter(Recipe.categoria_id == filtros["categoria"])

    if "tags" in filtros:
        termo = f"%{filtros['tags']}%"
        query = query.filter(Recipe.tags.ilike(termo))

    if "tempo_maximo" in filtros:
        query = query.filter(Recipe.tempo_preparacao <= filtros["tempo_maximo"])

    return query.order_by(Recipe.data_submetida.desc()).all()


def obter_receita_por_id(receita_id):
    return Recipe.query.get(receita_id)


def listar_receitas_por_utilizador(utilizador_id):
    return (
        Recipe.query.filter_by(utilizador_id=utilizador_id)
        .order_by(Recipe.data_submetida.desc())
        .all()
    )


def listar_pendentes():
    return (
        Recipe.query.filter_by(publicada=False)
        .order_by(Recipe.data_submetida.asc())
        .all()
    )
