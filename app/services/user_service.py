from app.models.user import User
from app.db import db


def criar_utilizador(nome, email, password, nivel=1):
    if User.query.filter_by(email=email).first():
        return None
    novo_utilizador = User(nome=nome, email=email, nivel=nivel)
    novo_utilizador.set_password(password)
    db.session.add(novo_utilizador)
    db.session.commit()
    return novo_utilizador


def validar_login(email, password):
    utilizador = User.query.filter_by(email=email).first()
    if utilizador and utilizador.check_password(password):
        if not utilizador.ativo:
            return "bloqueado"
        return utilizador
    return None


def obter_utilizador_por_id(user_id):
    return User.query.get(user_id)


def listar_todos_utilizadores():
    return User.query.order_by(User.criado_em.desc()).all()


def atualizar_dados_utilizador(
    user_id, novo_nome=None, novo_email=None, novo_nivel=None
):
    utilizador = User.query.get(user_id)
    if not utilizador:
        return None
    if novo_nome:
        utilizador.nome = novo_nome
    if novo_email:
        utilizador.email = novo_email
    if novo_nivel is not None:
        utilizador.nivel = novo_nivel
    db.session.commit()
    return utilizador


def alternar_estado_utilizador(user_id):
    utilizador = User.query.get(user_id)
    if utilizador:
        utilizador.ativo = not utilizador.ativo
        db.session.commit()


def eliminar_utilizador(user_id):
    utilizador = User.query.get(user_id)
    if utilizador:
        db.session.delete(utilizador)
        db.session.commit()
