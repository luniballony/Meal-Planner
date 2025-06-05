from flask import Blueprint, session, redirect, url_for, flash, render_template
from app import db
from app.models import Recipe, Favorites
from app.services.favorites_service import adicionar_favorito, remover_favorito
from app.forms.favorites_form import AdicionarFavoritoForm
from app.forms.remove_favorites_form import RemoverFavoritoForm

from app.services.recipe_service import obter_receita_por_id
from app.forms.block_recipe_form import BloquearReceitaForm


favorites_bp = Blueprint("favorites", __name__, url_prefix="/favorites")


@favorites_bp.route("/adicionar/<int:receita_id>", methods=["POST"])
def adicionar(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para adicionar favoritos.", "warning")
        return redirect(url_for("auth.login"))

    from app.models import BlockedRecipe

    bloqueada = BlockedRecipe.query.filter_by(
        utilizador_id=user_id, receita_id=receita_id
    ).first()
    if bloqueada:
        flash("Não pode adicionar uma receita bloqueada aos favoritos.", "warning")
        return redirect(url_for("recipes.listar"))

    adicionar_favorito(user_id, receita_id)
    flash("Receita adicionada aos favoritos!", "success")
    return redirect(url_for("recipes.listar"))


@favorites_bp.route("/ver", methods=["GET"])
def ver_favoritos():
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para ver os favoritos.", "warning")
        return redirect(url_for("auth.login"))

    favoritos = (
        db.session.query(Recipe)
        .join(Favorites)
        .filter(Favorites.utilizador_id == user_id)
        .all()
    )
    remover_form = RemoverFavoritoForm()
    return render_template(
        "recipes/favorites.html", receitas=favoritos, remover_form=remover_form
    )


@favorites_bp.route("/remover/<int:receita_id>", methods=["POST"])
def remover(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para remover favoritos.", "warning")
        return redirect(url_for("auth.login"))

    sucesso = remover_favorito(user_id, receita_id)

    if sucesso:
        flash("Receita removida dos favoritos.", "success")
    else:
        flash("A receita não estava nos seus favoritos.", "info")
    return redirect(url_for("favorites.ver_favoritos"))


# lista receita individual
@favorites_bp.route("/ver_receita_favorita/<int:receita_id>", methods=["GET"])
def ver_receita_favorita(receita_id): 
    user_id = session.get("user_id")
    receita = obter_receita_por_id(receita_id)

    if not user_id:
        flash("Precisa de iniciar sessão para ver as suas receitas favoritas.", "warning")
        return redirect(url_for("auth.login"))
    
    if not receita or (
        not receita.publicada
        and receita.utilizador_id != user_id
        and session.get("user_nivel") != 3
    ):
        flash("Receita não encontrada.", "danger")
        return redirect(url_for("recipes.listar"))
    
    remover_form = RemoverFavoritoForm()
    return render_template(
        "recipes/ver_favoritas.html",
        receita=receita,
        remover_form=remover_form
    )


# verifica se receita está marcada como favorita
@favorites_bp.route("/verificar_favorita/<int:receita_id>", methods=["GET"])
def verificar_favorita(receita_id): 
    user_id = session.get("user_id")
    receita = obter_receita_por_id(receita_id)

    if not user_id:
        flash("Precisas de iniciar sessão para avançar.", "warning")
        return redirect(url_for("auth.login"))
    
    if not receita or (
        not receita.publicada
        and receita.utilizador_id != user_id
        and session.get("user_nivel") != 3
    ):
        flash("Receita não encontrada.", "danger")
        return redirect(url_for("recipes.listar"))
    
    
    favorita = Favorites.query.filter_by(receita_id=receita_id, utilizador_id=user_id).first()
    return favorita is not None
    