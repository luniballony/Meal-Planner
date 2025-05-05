from flask import Blueprint, session, redirect, url_for, flash
from app.services.favorites_service import adicionar_favorito

favorites_bp = Blueprint("favorites", __name__, url_prefix="/favorites")

@favorites_bp.route("/adicionar/<int:receita_id>", methods=["POST"])
def adicionar(receita_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Precisas de iniciar sessão para adicionar favoritos.", "warning")
        return redirect(url_for("auth.login"))  # ou qualquer rota de login

    adicionar_favorito(user_id, receita_id)
    flash("Receita adicionada aos favoritos!", "success")
    return redirect(url_for("main.home"))

