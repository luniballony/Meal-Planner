from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.services.category_service import listar_categorias, obter_categoria_por_id
from app.services.recipe_service import listar_receitas

categories_bp = Blueprint("categories", __name__, url_prefix="/categorias")


@categories_bp.route("/")
def index():
    if "user_id" not in session:
        flash("Precisas de iniciar sessão para ver as categorias.", "warning")
        return redirect(url_for("auth.login"))

    categorias = listar_categorias()
    return render_template("categories/index.html", categorias=categorias)


@categories_bp.route("/<int:categoria_id>")
def ver(categoria_id):
    if "user_id" not in session:
        flash("Precisas de iniciar sessão para ver receitas.", "warning")
        return redirect(url_for("auth.login"))

    categoria = obter_categoria_por_id(categoria_id)
    if not categoria:
        flash("Categoria não encontrada.", "danger")
        return redirect(url_for("categories.index"))

    receitas = [r for r in listar_receitas() if r.categoria_id == categoria_id]
    return render_template(
        "categories/ver.html", categoria=categoria, receitas=receitas
    )
