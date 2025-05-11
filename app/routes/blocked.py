from flask import Blueprint, session, redirect, url_for, flash, render_template
from app import db
from app.models import Recipe, blocked_recipe
from app.services.blocked_service import desbloquear_receita, listar_nao_bloqueadas, listar_bloqueadas, bloquear_receita
from app.forms.block_recipe_form import BloquearReceitaForm
from app.forms.unblock_form import DesbloquearReceitaForm

from app.services.blocked_service import (
    bloquear_receita,
    listar_bloqueadas,
    desbloquear_receita,
    listar_nao_bloqueadas,
)

from app.services.recipe_service import (
    obter_receita_por_id,
)

blocked_bp = Blueprint("blocked", __name__, url_prefix="/blocked")


@blocked_bp.route("/bloquear/<int:receita_id>", methods=["POST"])
def bloquear(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para bloquear receitas.", "warning")
        return redirect(url_for("auth.login"))

    bloquear_receita(user_id, receita_id)
    flash("Receita bloqueada com sucesso!", "success")
    return redirect(url_for("recipes.listar"))


@blocked_bp.route("/bloqueadas")
def bloqueadas():
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para ver receitas bloqueadas.", "warning")
        return redirect(url_for("auth.login"))

    receitas = listar_bloqueadas(user_id)
    form = DesbloquearReceitaForm()
    return render_template("recipes/bloqueadas.html", receitas=receitas, form=form)


@blocked_bp.route("/desbloquear/<int:receita_id>", methods=["POST"])
def desbloquear(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para desbloquear receitas.", "warning")
        return redirect(url_for("auth.login"))

    sucesso = desbloquear_receita(user_id, receita_id)

    if sucesso:
        flash("Receita desbloqueada com sucesso!", "success")
    else:
        flash("A receita não estava bloqueada.", "info")
    return redirect(url_for("blocked.bloqueadas"))


# lista receita individual
@blocked_bp.route("/ver_receita_bloqueada/<int:receita_id>", methods=["GET"])
def ver_receita_bloqueada(receita_id): 
    user_id = session.get("user_id")
    receita = obter_receita_por_id(receita_id)

    if not user_id:
        flash("Precisas de iniciar sessão para ver as tuas receitas bloqueadas.", "warning")
        return redirect(url_for("auth.login"))
    
    if not receita or (
        not receita.publicada
        and receita.utilizador_id != user_id
        and session.get("user_nivel") != 3
    ):
        flash("Receita não encontrada.", "danger")
        return redirect(url_for("recipes.listar"))
    

    form = DesbloquearReceitaForm()
    return render_template(
        "recipes/ver_bloqueadas.html",
        receita=receita,
        form=form
    )
